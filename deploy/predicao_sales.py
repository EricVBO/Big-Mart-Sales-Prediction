import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='template', static_folder='template/assets')

# Treina lá, usa cá
modelo_pipeline = pickle.load(open('./models/pipe.pkl', 'rb'))

@app.route('/dados_produto')
def dados_produto():
    return render_template("form.html")

def get_data():
    Item_Weight = request.form.get('Item_Weight')
    Item_Fat_Content= request.form.get('Item_Fat_Content')
    Item_Visibility= request.form.get('Item_Visibility')
    Item_Type= request.form.get('Item_Type')
    Item_MRP= request.form.get('Item_MRP')
    Outlet_Identifier= request.form.get('Outlet_Identifier',)
    Outlet_Establishment_Year= request.form.get('Outlet_Establishment_Year')
    Outlet_Size= request.form.get('Outlet_Size')
    Outlet_Location_Type= request.form.get('Outlet_Location_Type')
    Outlet_Type= request.form.get('Outlet_Type')

    
    d_dict = {'Item_Weight': [Item_Weight], 'Item_Fat_Content': [Item_Fat_Content],
              'Item_Visibility': [Item_Visibility],
              'Item_Type': [Item_Type], 'Item_MRP': [Item_MRP], 'Outlet_Identifier': [Outlet_Identifier],
              'Outlet_Establishment_Year': [Outlet_Establishment_Year], 'Outlet_Size': [Outlet_Size],
              'Outlet_Location_Type': [Outlet_Location_Type], 'Outlet_Type': [Outlet_Type]}
    return pd.DataFrame.from_dict(d_dict, orient='columns')

@app.route('/send', methods=['POST'])
def show_data():
    df = get_data()
    
    df = df[['Item_Weight', 'Item_Fat_Content', 'Item_Visibility', 'Item_Type', 'Item_MRP',
             'Outlet_Identifier', 'Outlet_Establishment_Year', 'Outlet_Size', 'Outlet_Location_Type',
             'Outlet_Type']]


    prediction = modelo_pipeline.predict(df)
    result = format(prediction[0], '.0f')
    result_text = str(result) + '  vendas previstas.'

    return render_template('result.html', tables=[df.to_html(classes='data', header=True, col_space=10)],
                           result= result_text)


if __name__ == "__main__":
    app.run(debug=True)
