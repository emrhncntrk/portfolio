//Graph logic
function get_graph(symbol, period){
    fetch(`/get_graph/${symbol}/${period}`)
    .then(response=> response.json())
    .then(data => {
        const stock_data = JSON.parse(data.stock_data);
        const trace = {
            x: stock_data.index,
            y: stock_data.data,
            mode: 'lines',
            type: 'scatter'
        };
        var data = [trace];
        const layout = {
            title: `${symbol} Price Chart`,
            //Styling for ploty chart is made here
            margin: {
                l: 40,
                r: 40,
                t: 40,
                b: 40
            },
            font: {
                family: 'Sen, sans-seriff',
                size: 14,
              }
        };
        Plotly.newPlot('stock-graph', data, layout, { responsive: true });
    })
    .catch(error => {
        throw new Error('Failed to fetch data');
    });
}
//Arbitrage graph logic
function get_arbitrage(xSymbol, ySymbol, period){
    fetch(`/get_arbitrage/${xSymbol}/${ySymbol}/${period}`)
    .then(response=> response.json())
    .then(data => {
        const stock_data = JSON.parse(data.stock_data);
        const trace = {
            x: stock_data.index,
            y: stock_data.data,
            mode: 'lines',
            type: 'scatter'
        };
        var data = [trace];
        const layout = {
            title: `${xSymbol}/${ySymbol} Ratio`,
            //Styling
            margin: {
                l: 40,
                r: 40,
                t: 40,
                b: 40
            },
            font: {
                family: 'Sen, sans-seriff',
                size: 14,
              }
        };
        Plotly.newPlot('stock-graph', data, layout, { responsive: true });

        document.querySelector('#stock-info').style.display = 'none';
        document.querySelector('#add-button').style.display = 'none'; 
        document.querySelector('#arbitrageSymbol').innerHTML = ySymbol;
        document.querySelector('#arbitragefield').value = '';
        document.querySelector('#arbSearchError').innerHTML = '';
    })
    .catch(error => {
        document.querySelector('#arbSearchError').innerHTML = "Symbol not found!";
    });
}

//Hiding views and displaying a loading element.
function hide_all(){
    document.querySelector('#stock-detail-view').style.display = 'none';
    document.querySelector('#stocks-list').style.display = 'none';
    document.querySelector('#portfolio-list').style.display = 'none';
    document.querySelector('#add-button').style.display = 'none';
    document.querySelector('#load-view').style.display = 'block';
    document.querySelector('#success').textContent = ''; 
}

//Get the csrf token value from the cookies
function getCsrf(){
    const value= `; ${document.cookie}`;
    const parts = value.split('; csrftoken=');
    if(parts.length == 2) return parts.pop().split(';').shift();       
}
    
//Get details of a stock.
function get_detail(symbol){
    //Period is 1 day by default
    const period = '1d';
    const errorDiv = document.querySelector('#searchError');
    fetch(`/get_stock_info/${symbol}`) 
        .then(response => {
            if (response.ok) {
            errorDiv.innerHTML= '';
            return response.json();
            } else {
            //Display an error if symbol does not exist
            errorDiv.innerHTML = 'Symbol not found!';
            throw new Error('Failed to fetch data');
            }
        })
        .then(data => {
            
            document.querySelector('#stocks-list').style.display = 'none';
            document.querySelector('#portfolio-list').style.display = 'none';
            document.querySelector('#stock-detail-view').style.display = 'block';

            const auth = document.querySelector('#authentication').textContent;
            if (auth === "yes") {
                document.querySelector('#add-button').style.display = 'block';
            }
            
            const stock_info = document.querySelector('#stock-info')
            //Check if symbol is a stock or not and display data accordingly
            if(symbol.includes("=")){      
                stock_info.innerHTML = `
                <h1 id="symbolDetail">${data.symbol}</h1>
                <h1 id="arbitrageSymbol"></h1>
                <ul class="detail-list">
                    <li><span class="subject">Symbol:</span> ${data.symbol}</li>
                    <li><span class="subject">Opening:</span> ${data.open}</li>
                    <li><span class="subject">Previous:</span> ${data.previous}</li>
                    <li><span class="subject">Today High:</span> ${data.dayHigh}</li>
                    <li><span class="subject">Today Low:</span> ${data.dayLow}</li>
                    <li><span class="subject">Fifty Day Average:</span> ${data.fiftyDayAverage}</li>
                </ul>
                `;
            }else{
                stock_info.innerHTML = `
                <h1 id="symbolDetail">${data.symbol}</h1>
                <h1 id="arbitrageSymbol"></h1>
                <ul class="detail-list">
                    <li><span class="subject">Symbol:</span> ${data.symbol}</li>
                    <li><span class="subject">Name:</span> ${data.name}</li>
                    <li><span class="subject">Price:</span> ${data.price}</li>
                    <li><span class="subject">Previous:</span> ${data.previous}</li>
                    <li><span class="subject">Today High:</span> ${data.dayHigh}</li>
                    <li><span class="subject">Today Low:</span> ${data.dayLow}</li>
                    <li><span class="subject">Target Price:</span> ${data.targetHighPrice}</li>
                    <li><span class="subject">Fifty Day Average:</span> ${data.fiftyDayAverage}</li>
                    <li><span class="subject">Volume:</span> ${data.volume}</li>
                    <li><span class="subject">Average Volume:</span> ${data.averageVolume}</li>
                    <li><span class="subject">Market Cap:</span> ${data.marketCap}</li>
                    <li><span class="subject">Total Revenue:</span> ${data.totalRevenue}</li>
                    <li><span class="subject">Operating Cashflow:</span> ${data.operatingCashflow}</li>
                </ul>
                `;
            }
            document.querySelector('#stock-info').style.display = 'block';
            const buttonValue = document.querySelector('#add-button');
            let portfolio_data = [];
                fetch('get_portfolio/')
            .then(response => {
            if (response.ok) {
                get_graph(symbol, period);
                return response.json();
            } else {
                throw new Error('Failed to fetch data');
            }
            })
            .then(data =>{
                portfolio_data = data;
            
            console.log(portfolio_data);
            
            const upperSymbol = symbol.toUpperCase();
            console.log(upperSymbol);
            if (portfolio_data.includes(upperSymbol)) {
                buttonValue.innerHTML= `<button id="addButton" type="submit" class="btn btn-primary">Remove</button>`
            }else{
                buttonValue.innerHTML= `<button id="addButton" type="submit" class="btn btn-primary">Add</button>`
            };
             //Add or remove a stock from portfolio.
            document.querySelector('#addButton').addEventListener('click', function(){
            const action = document.querySelector('#addButton').textContent;     
                fetch('/add_stock/',{
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrf(), 
                    },
                    body: JSON.stringify({
                        action: `${action}`,
                        symbol: `${upperSymbol}`,
                    })
                })
                .then(response => response.json())
                .then(result =>{
                    if(action === 'Add'){
                        document.querySelector('#addButton').innerHTML = 'Remove';
                        document.querySelector('#success').textContent = 'Added to portfolio!';
                        
                    }else{
                        document.querySelector('#addButton').innerHTML = 'Add';
                        document.querySelector('#success').textContent = 'Removed from portfolio!';
                    }
                    
                  
                    console.log(result);
                })

            })
        
        })
        .catch(error => {
            console.error(error);
        });
    
    })
    

}
//Get Index Components
function get_index(index){
    hide_all();
    document.querySelector('#arbSearchError').innerHTML = '';
    document.querySelector('#searchError').innerHTML = '';
    fetch(`/get_index/${index}`) 
    .then(response => {
        if (response.ok) {
        return response.json();
        } else {
        throw new Error('Failed to fetch data');
        }
    })
    .then(data => {
        document.querySelector('#data-table tbody').innerHTML = ''
        const table = document.querySelector('#data-table tbody');
        console.log(data)

        data.stocks.forEach(item => {
            const row = document.createElement('tr');

            row.addEventListener('click', () => {
            get_detail(item.symbol);
            }); 
           

            row.innerHTML=`
                <td>${item.symbol}</td>
                <td>${item.companyName}</td>
                <td class="price ${item.deltaIndicator}">${item.lastSalePrice}</td>
            `;
            
            table.appendChild(row);
             
        })
        document.querySelector('#load-view').style.display = 'none';
        document.querySelector('#stocks-list').style.display = 'block';

    })
    .catch(error => {
        console.error(error);
    });
}

document.addEventListener("DOMContentLoaded", function(){

    //Authentication check.
    const auth = document.querySelector('#authentication').textContent;

    //Get Nasdaq Index Components by default.
    get_index("nasdaq");

    document.querySelector('#pageTitle').addEventListener('click', function(){
        get_index("nasdaq");
    })

    //Searching logic.
    document.querySelector('#searchform').addEventListener('submit', function(){
        event.preventDefault();
        const symbol = document.querySelector('#searchfield').value.toUpperCase();
        document.querySelector('#stock-info').style.display = 'block';
        document.querySelector('#searchfield').value = '';
        document.querySelector('#success').textContent = '';
        try {
            get_detail(symbol)
        }catch (error) {
            console.error(error);
        }
        
    });
    //Nasdaq button.
    document.querySelector('#nasdaqButton').addEventListener('click', function(){
        get_index("nasdaq");
    })
    //Currencies button.
    document.querySelector('#currenciesButton').addEventListener('click', function(){
        get_index("currencies");
    })
    //Futures button.
    document.querySelector('#futuresButton').addEventListener('click', function(){
        get_index("futures");
    })

    //Chart period buttons.
    const buttons = document.querySelectorAll('.periodButton');
    buttons.forEach(function(button) {
        button.addEventListener("click", function() {
            const period = button.value;
            const xSymbol = document.querySelector('#symbolDetail').innerHTML;
            if(document.querySelector('#stock-info').style.display === 'none'){
                const ySymbol = document.querySelector('#arbitrageSymbol').innerHTML;
                get_arbitrage(xSymbol,ySymbol,period);
            }else{
                get_graph(xSymbol,period);
            }
        })

    })
    //Arbitrage logic.
    document.querySelector('#arbitrageform').addEventListener('submit', function(){
        event.preventDefault();
        const xSymbol = document.querySelector('#symbolDetail').innerHTML;
        const ySymbol = document.querySelector('#arbitragefield').value.toUpperCase();
        document.querySelector('#success').textContent = '';
        const period = '1d';
        
        get_arbitrage(xSymbol,ySymbol,period);

        
    });


    //View user portfolio.
    if (auth === "yes"){
        document.querySelector('#portfolioButton').addEventListener('click', function(){
            event.preventDefault();
            hide_all()
            fetch('get_portfolio/')
            .then(response => {
            if (response.ok) {
            return response.json();
            } else {
            throw new Error('Failed to fetch data');
            }
            })
            .then(data =>{
                const symbolsList = data;
                const table = document.querySelector('#portfolio-table tbody');
                table.innerHTML="" ;
            
            symbolsList.forEach(symbol => {
                fetch(`/get_stock_info/${symbol}`) 
                .then(response => {
                    if (response.ok) {
                    return response.json();
                    } else {
                    throw new Error('Failed to fetch data');
                    }
                })
                .then(data => {
                    

                    const row = document.createElement('tr');

                    row.addEventListener('click', () => {
                    get_detail(data.symbol);
                    });
                    if(symbol.includes("=")){
                        row.innerHTML=`
                            <td>${data.symbol}</td>
                            <td>${data.name}</td>
                            <td class="price ${data.indicator}">${data.price}</td>
                        `;

                    }else{
                        row.innerHTML=`
                            <td>${data.symbol}</td>
                            <td>${data.name}</td>
                            <td class="price ${data.indicator}">${data.price}</td>
                        `;
                    }
                    table.appendChild(row);
                

                })
                .catch(error => {
                    console.error(error);
                });

            })
            document.querySelector('#load-view').style.display = 'none';
            document.querySelector('#portfolio-list').style.display = 'block';
        })
            
        });
    };

}); 

