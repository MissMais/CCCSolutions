from django.shortcuts import render, redirect
from financetoolkit import Toolkit
from .Api import API_KEY


# Create your views here.
def home(request):
    if request.method == 'POST':
        ticker = request.POST['search']
    
        comp = Toolkit([ticker], api_key=API_KEY, start_date="2015-01-01")
        q_comp = Toolkit([ticker], api_key=API_KEY, start_date="2005-01-01", quarterly=True)

        # downloading data from api
        t_profile = comp.get_profile()
        t_data = comp.get_historical_data()

        ratio = q_comp.ratios.collect_valuation_ratios()
        current_eps = ratio.loc['Earnings per Share (EPS)'].tail(1).values[0]
        print (current_eps)
        p_e = t_data['Close'].tail(1).values[0][0]/current_eps

        bookVal = ratio.loc['Book Value per Share',:].tail(1).values[0]

        ratio2 = q_comp.ratios
        r = ratio2.collect_profitability_ratios()
        roce = r.loc['Return on Capital Employed (ROCE)'].tail(1).values[0]
        roe = r.loc['Return on Equity (ROE)'].tail(1).values[0]

        # comp_data = {'name': t_profile[ticker]['Company Name'],
        #              'sector': t_profile[ticker]['Sector'],
        #              'industry': t_profile[ticker]['Industry'],
        #              'exchange': t_profile[ticker]['Exchange Short Name'],
        #              'high': t_data['High'].tail(1).values[0],
        #              'low': t_data['Low'].tail(1).values[0],
        #              'close': t_data['Close'].tail(1).values[0],}
        # print(comp_data)

        return render(request, 'index.html', {'name': t_profile[ticker]['Company Name'],
                    'sector': t_profile[ticker]['Sector'],
                    'industry': t_profile[ticker]['Industry'],
                    'exchange': t_profile[ticker]['Exchange Short Name'],
                    'cap':t_profile[ticker]['Market Capitalization'],
                    'high': t_data['High'].tail(1).values[0],
                    'low': t_data['Low'].tail(1).values[0],
                    'close': t_data['Close'].tail(1).values[0],
                    'p_e':p_e,
                    'bookVal':bookVal,
                    'roce':roce,
                    'roe':roe})
    
    return render(request, 'index.html')
