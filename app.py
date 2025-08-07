import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_cors import CORS
from services.pinpag_api import PinPagAPI

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure CORS for integration with external websites
CORS(app, origins="*")  # Configure with your specific domain in production

# Initialize PinPag API service
pinpag_api = PinPagAPI()

@app.route('/')
def index():
    """Main page with vehicle consultation form"""
    return render_template('index.html')

@app.route('/consultar', methods=['POST'])
def consultar():
    """Handle vehicle consultation request"""
    try:
        # Get form data
        uf = request.form.get('uf', 'SP').upper()
        renavam = request.form.get('renavam', '').strip()
        license_plate = request.form.get('license_plate', '').strip().upper()
        
        # Validation
        if not renavam and not license_plate:
            flash('Por favor, informe o RENAVAM ou a placa do veículo.', 'danger')
            return redirect(url_for('index'))
        
        if uf != 'SP':
            flash('Atualmente, apenas veículos cadastrados em SP são aceitos.', 'warning')
            return redirect(url_for('index'))
        
        # Step 1: Request vehicle consultation
        app.logger.info(f"Requesting vehicle consultation for UF: {uf}, RENAVAM: {renavam}, Plate: {license_plate}")
        
        consult_response = pinpag_api.request_vehicle_consultation(
            uf=uf,
            renavam=renavam if renavam else None,
            license_plate=license_plate if license_plate else None
        )
        
        if not consult_response or 'consult_id' not in consult_response:
            flash('Erro ao solicitar consulta do veículo. Tente novamente.', 'danger')
            return redirect(url_for('index'))
        
        consult_id = consult_response['consult_id']
        app.logger.info(f"Consultation requested successfully. Consult ID: {consult_id}")
        
        # Step 2: Get consultation results with retry logic
        app.logger.info(f"Fetching consultation results for ID: {consult_id}")
        
        debits_response = pinpag_api.get_vehicle_debits_with_retry(consult_id)
        
        if not debits_response:
            flash('Erro ao obter os débitos do veículo. Tente novamente.', 'danger')
            return redirect(url_for('index'))
        
        # Store consultation data in session
        session['consultation_data'] = {
            'consult_id': consult_id,
            'vehicle': debits_response.get('vehicle'),
            'debits': debits_response.get('debits', []),
            'warnings': debits_response.get('warnings', []),
            'flags': debits_response.get('flags', {})
        }
        
        return redirect(url_for('results'))
        
    except Exception as e:
        app.logger.error(f"Error in consultation: {str(e)}")
        flash('Erro interno do servidor. Tente novamente mais tarde.', 'danger')
        return redirect(url_for('index'))

@app.route('/resultados')
def results():
    """Display consultation results"""
    consultation_data = session.get('consultation_data')
    
    if not consultation_data:
        flash('Nenhuma consulta encontrada. Realize uma nova consulta.', 'warning')
        return redirect(url_for('index'))
    
    return render_template('results.html', data=consultation_data)

@app.route('/gerar-link', methods=['POST'])
def gerar_link():
    """Generate payment link for selected debits"""
    try:
        consultation_data = session.get('consultation_data')
        
        if not consultation_data:
            flash('Sessão expirada. Realize uma nova consulta.', 'warning')
            return redirect(url_for('index'))
        
        selected_debits = request.form.getlist('selected_debits')
        
        if not selected_debits:
            flash('Selecione pelo menos um débito para gerar o link de pagamento.', 'warning')
            return redirect(url_for('results'))
        
        # Generate payment link
        payment_link = pinpag_api.generate_payment_link(
            consult_id=consultation_data['consult_id'],
            debit_ids=selected_debits
        )
        
        if payment_link and 'link' in payment_link:
            flash('Link de pagamento gerado com sucesso!', 'success')
            session['payment_link'] = payment_link['link']
        else:
            flash('Erro ao gerar link de pagamento. Tente novamente.', 'danger')
        
        return redirect(url_for('results'))
        
    except Exception as e:
        app.logger.error(f"Error generating payment link: {str(e)}")
        flash('Erro ao gerar link de pagamento. Tente novamente.', 'danger')
        return redirect(url_for('results'))

@app.route('/nova-consulta')
def nova_consulta():
    """Clear session and start new consultation"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Use dynamic port for cloud deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
