from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import pandas as pd
import numpy as np
from myApp.forms import add_port, add_comp
from django.shortcuts import redirect


def home(request):
    return render(request, "home.html")


from django.shortcuts import render


def search_stock(request):
    ticker_symbol = request.GET.get('ticker', '')
    if ticker_symbol:
        chart_url, result = print_stock(ticker_symbol)
        form = add_port()
        form2 = add_comp()
       
        if chart_url and result:

            if request.method == 'POST':

                if 'save' in request.POST:
                    form = add_port(request.POST)
                    form.save()
                elif 'delete' in request.POST:
                    pk = request.POST.get('delete')
                    port = Portfolio.objects.get(portfolio_id=pk)
                    port.delete()
                elif 'add' in request.POST:
                    form2 = add_comp(request.POST)

                    if form2.is_valid():
                        form2.save()
                    # else:
                    #     form2 = add_comp()


            
            return render(request, 'stock_search.html', {
                'chart_url': chart_url,
                'stock_data': result,
                'rsi': momentum_trading(request),
                'zscore': mean_reversion(request),
                'minmax': support_and_resistance(request),
                'ports' : portfolio_list(request),
                'form':form,
                'form2':form2
            })
        else:
            return render(request, 'stock_search.html', {'error': result})  
    else:
        return render(request, 'stock_search.html', {'error': 'No ticker symbol provided.'})


def autocomplete(request):
    if 'term' in request.GET:
        qs = Share.objects.filter(ticker__icontains=request.GET.get('term')).order_by('ticker')[:3]
        tickers = list(qs.values_list('ticker', flat=True))
        return JsonResponse(tickers, safe=False)
    return JsonResponse([], safe=False)


import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64




def print_stock(ticker_symbol):
    try:
        share = Share.objects.get(ticker=ticker_symbol)


        # Correctly get the company instance associated with the share
        company = share.id


        data_entries = Data.objects.filter(ticker=ticker_symbol).order_by('date')
       
        if not data_entries.exists():
            return None, "No data available for the ticker symbol entered."  # Ensure two values are returned
       
        # Generate the plot
        fig, ax = plt.subplots()
        ax.plot([entry.date for entry in data_entries], [entry.close_price for entry in data_entries])
        ax.set(title=f'Stock Data for {company.name}', xlabel='Date', ylabel='Price')


        plt.xticks(rotation=45)


        plt.xticks(fontsize=6)




       
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
       
        # Encode the image as base64 to embed in HTML
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        chart_url = f"data:image/png;base64,{image_base64}"
       
        return chart_url, data_entries.last()  # Ensure two values are returned
    except Share.DoesNotExist:
        return None, "Ticker symbol not found."  # Ensure two values are returned
    except Exception as e:
        return None, str(e)  # Ensure two values are returned, convert exception to string












































































# def search_stock(request):
#     # Fetch the ticker symbol from the request
#     ticker_symbol = request.GET.get('ticker')
#     if ticker_symbol:
#         # Query the database for stock data corresponding to the ticker
#         stock_data = Data.objects.filter(ticker__ticker__iexact=ticker_symbol).order_by('-date').first()
#         if stock_data:
#             context = {
#                 'stock_data': stock_data,
#                 'rsi': momentum_trading(request),
#                 'zscore': mean_reversion(request),
#                 'minmax': support_and_resistance(request)
#             }
#             return render(request, 'stock_search.html', context)
#         else:
#             return render(request, 'stock_search.html', {'error': 'No data found'})
#     else:
#         return render(request, 'stock_search.html', {'error': 'No ticker provided'})




# def autocomplete(request):
#     if 'term' in request.GET:
#         qs = Share.objects.filter(ticker__icontains=request.GET.get('term')).order_by('ticker')[:3]
#         tickers = list(qs.values_list('ticker', flat=True))
#         return JsonResponse(tickers, safe=False)
#     return JsonResponse([], safe=False)








































def momentum_trading(request):
    ticker_symbol = request.GET.get('ticker')


    if ticker_symbol:
        ticker_data = Data.objects.filter(ticker__ticker__iexact=ticker_symbol).order_by('-date')[:14]


        data_dict = {
            'Date': [data_instance.date for data_instance in ticker_data],
            'Close': [data_instance.close_price for data_instance in ticker_data],
        }


        data_df = pd.DataFrame(data_dict)


        data_df_reversed = data_df[::-1]


        data_df_reversed['Price Change'] = data_df_reversed['Close'].diff()


        # Separate gains and losses
        data_df_reversed['Gain'] = data_df_reversed['Price Change'].apply(lambda x: x if x > 0 else 0)
        data_df_reversed['Loss'] = data_df_reversed['Price Change'].apply(lambda x: abs(x) if x < 0 else 0)


        # Calculate average gain and average loss over the period of DataFrame length
        period = len(data_df_reversed)
       
        data_df_reversed['Avg Gain'] = data_df_reversed['Gain'].rolling(window=period).mean()
        data_df_reversed['Avg Loss'] = data_df_reversed['Loss'].rolling(window=period).mean()


        # Calculate Relative Strength (RS)
        data_df_reversed['RS'] = data_df_reversed['Avg Gain'] / data_df_reversed['Avg Loss']


        # Calculate RSI for the final date (final row)
        last_date_rsi = 100 - (100 / (1 + data_df_reversed.iloc[-1]['RS']))




        return last_date_rsi




def mean_reversion(request):
    ticker_symbol = request.GET.get('ticker')


    if ticker_symbol:
        ticker_data = Data.objects.filter(ticker__ticker__iexact=ticker_symbol).order_by('-date')


        data_dict = {
            'Date': [data_instance.date for data_instance in ticker_data],
            'Close': [data_instance.close_price for data_instance in ticker_data],
        }


        data_df = pd.DataFrame(data_dict)


        data_df['Close'] = data_df['Close'].astype(float)




        data_df_reversed = data_df[::-1]


        # Define window size for rolling calculations
        window_size = len(data_df_reversed)


        # Calculate rolling mean
        data_df_reversed['mean'] = data_df_reversed['Close'].rolling(window=window_size).mean()
       
        # Calculate rolling standard deviation
        data_df_reversed['std'] = data_df_reversed['Close'].rolling(window=window_size).std()


        # Calculate z-score
        data_df_reversed['z_score'] = (data_df_reversed['Close'] - data_df_reversed['mean']) / data_df_reversed['std']


        # Return the most recent z-score (last row of the 'z_score' column)
        return data_df_reversed['z_score'].iloc[-1]


def support_and_resistance(request):
    ticker_symbol = request.GET.get('ticker')
    min_value, max_value = None, None


    if ticker_symbol:
        # Retrieve ticker data from the database
        ticker_data = Data.objects.filter(ticker__ticker__iexact=ticker_symbol).order_by('-date')


        # Create a DataFrame from the retrieved data
        data_dict = {
            'Date': [data_instance.date for data_instance in ticker_data],
            'Close': [data_instance.close_price for data_instance in ticker_data],
            'High': [data_instance.high for data_instance in ticker_data],
            'Low': [data_instance.low for data_instance in ticker_data],
        }
        data_df = pd.DataFrame(data_dict)


        # Reverse the DataFrame
        data_df = data_df[::-1]


        # Convert columns to float if needed
        data_df['Close'] = data_df['Close'].astype(float)
        data_df['High'] = data_df['High'].astype(float)
        data_df['Low'] = data_df['Low'].astype(float)


        # Define the window size for rolling calculations
        window = len(data_df)


        # Calculate support and resistance levels
        min_value, max_value = calculate_support_resistance(data_df, window)


    return 'floor val: ' , min_value, ' ceiling val:', max_value


def calculate_support_resistance(data_df, window):
    # Calculate support and resistance levels
    data_df['High_Max'] = data_df['High'].rolling(window=window).max()
    data_df['Low_Min'] = data_df['Low'].rolling(window=window).min()
   
    # Get the min and max values
    min_value = data_df['Low_Min'].iloc[-1]
    max_value = data_df['High_Max'].iloc[-1]


    return min_value, max_value


# def trend_following(request):


#     ticker_symbol = request.GET.get('ticker')


#     if ticker_symbol:
#         ticker_data = Data.objects.filter(ticker__ticker__iexact=ticker_symbol).order_by('-date')


#         data_dict = {
#             'Date': [data_instance.date for data_instance in ticker_data],
#             'Close': [data_instance.close_price for data_instance in ticker_data],
#         }


#         data_df = pd.DataFrame(data_dict)


#         data_df['Close'] = data_df['Close'].astype(float)




#         data_df_reversed = data_df[::-1]


#Need more data for trend following. Will revisit.






# def add_portfolio(request, name):


    # largest_index = Data.objects.aggregate(largest_index=Max('id'))['largest_index']





def portfolio_list(request):
    portfolios = Portfolio.objects.all()
    return portfolios








def portfolio(request):
    portfolio_id = request.GET.get('portfolio_id')

    if request.method == 'POST':
        if 'remove' in request.POST:
            portfolio_id = request.POST.get('portfolio_id')
            ticker = request.POST.get('ticker')
    
            portfolio = Portfolio.objects.get(pk=portfolio_id)
            share = Share.objects.get(ticker=ticker)
    
            portfolio.composition.remove(share)

    portfolio_contents = Composed_of.objects.filter(portfolio_id=portfolio_id)

    context = {
        'portfolio_id': portfolio_id,
        'portfolio_contents': portfolio_contents, 
    }
    return render(request, 'portfolio.html', context)

















