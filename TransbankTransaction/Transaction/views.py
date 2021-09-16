from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect  # for return response to client

from .forms import PaymentForm

#for dealing with transaction.
from transbank.transaccion_completa.transaction import Transaction

def index(request):
    return render(request, 'index.html')

def doTransaction(request):
    if request.method == "GET":
        form = PaymentForm()
        return render(request, 'payment_form.html', context = {'form' : form})
    elif request.method == "POST":
        form = PaymentForm(request.POST)
        if not form.is_valid():
            context = {'form' : form}
            return render(request, "payment_form.html", context = context)
        c_data = form.cleaned_data
        buy_order = 'order0'
        session_id = 'session0'
        amount = c_data['amount']
        card_number = c_data['card_number']
        cvv = c_data['cvv']
        card_expiration_date = c_data['card_expiration']

        #Step 1: Create Transaction
        respTr = Transaction.create(
        buy_order=buy_order, session_id=session_id, amount=amount,
        card_number=card_number, cvv=cvv, card_expiration_date=card_expiration_date)


        #Step 2: set installments
        token = respTr.token
        installments_number = 2
        respIns = Transaction.installments(token=token, installments_number=installments_number)

        #Step 3: commit transaction
        id_query_installments = respIns.id_query_installments
        deferred_period_index = respIns.deferred_periods
        grace_period = 'false'
        respCommit = Transaction.commit(token=token,
                          id_query_installments=id_query_installments,
                          deferred_period_index=deferred_period_index,
                          grace_period=grace_period)
        #Step 4: give user info about commit
        context = {'amount' : amount, 'respCommit' :  respCommit}
        return render(request, "payment_response.html", context =  context)
