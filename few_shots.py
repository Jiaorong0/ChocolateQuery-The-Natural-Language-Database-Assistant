few_shots = [
    {'Question' : "How many 100g Lindt Milk Chocolate bars do we have in stock?",
     'SQLQuery' : "SELECT stock_quantity FROM chocolates WHERE brand = 'Lindt' AND flavor = 'Milk Chocolate' AND weight = '100g';"
    },
    {'Question': "What is the total price of the inventory for all Dark Chocolate bars?",
     'SQLQuery':"SELECT SUM(price * stock_quantity) FROM chocolates WHERE flavor = 'Dark Chocolate';"
    },
    {'Question': "If we have to sell all the Hershey chocolates today with discounts applied, how much revenue will our store generate (post discounts)?" ,
     'SQLQuery' : """SELECT SUM(a.total_amount * ((100 - COALESCE(d.pct_discount, 0)) / 100)) AS total_revenue
FROM (SELECT SUM(price * stock_quantity) AS total_amount, chocolate_id 
FROM chocolates WHERE brand = 'Hershey' 
GROUP BY chocolate_id) a
LEFT JOIN discounts d ON a.chocolate_id = d.chocolate_id;
 """
    },
     {'Question' : "If we sell all the Cadbury chocolates today, how much revenue will our store generate without any discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM chocolates WHERE brand = 'Cadbury';"
     },
    {'Question': "How many 50g White Chocolate bars of Godiva do we have?",
     'SQLQuery' : "SELECT stock_quantity FROM chocolates WHERE brand = 'Godiva' AND flavor = 'White Chocolate' AND weight = '50g';"
    }
]