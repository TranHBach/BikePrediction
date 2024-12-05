import pandas as pd

def analyze_shipping_performance():
    """Analyze shipping methods based on rejection rates"""
    
    # Load required data
    purchase_order_detail = pd.read_csv('purchaseOrderDetail.csv')
    purchase_order_header = pd.read_csv('purchaseOrderHeader.csv')
    ship_method = pd.read_csv('shipMethod.csv')
    
    # Merge relevant data
    shipping_analysis = (purchase_order_detail.merge(
        purchase_order_header[['PurchaseOrderID', 'ShipMethodID']], 
        on='PurchaseOrderID'
    ).merge(
        ship_method[['ShipMethodID', 'Name']], 
        on='ShipMethodID'
    ))
    
    # Calculate metrics per shipping method
    shipping_metrics = []
    for method_id, method_data in shipping_analysis.groupby('ShipMethodID'):
        method_name = method_data['Name'].iloc[0]
        
        # Calculate rejection rate
        total_orders = method_data['OrderQty'].sum()
        rejected_qty = method_data['RejectedQty'].sum()
        rejection_rate = (rejected_qty / total_orders * 100) if total_orders > 0 else 0
        
        shipping_metrics.append({
            'ShipMethodID': method_id,
            'Name': method_name,
            'Total_Orders': int(total_orders),
            'Rejected_Quantity': int(rejected_qty),
            'Rejection_Rate': round(rejection_rate, 2)
        })
    
    # Convert to DataFrame and sort by rejection rate
    metrics_df = pd.DataFrame(shipping_metrics)
    metrics_df = metrics_df.sort_values('Rejection_Rate')
    
    # Print analysis results
    print("\nShipping Method Rejection Rates")
    print("==============================")
    
    for _, method in metrics_df.iterrows():
        print(f"\nShipping Method: {method['Name']}")
        print(f"Total Orders: {method['Total_Orders']}")
        print(f"Rejected Quantity: {method['Rejected_Quantity']}")
        print(f"Rejection Rate: {method['Rejection_Rate']}%")
    
    # Get best method (lowest rejection rate)
    best_method = metrics_df.iloc[0]
    
    print("\nRecommendation:")
    print("===============")
    print(f"Recommended Shipping Method: {best_method['Name']}")
    print(f"Rejection Rate: {best_method['Rejection_Rate']}%")
    
    return metrics_df

if __name__ == "__main__":
    shipping_metrics = analyze_shipping_performance()
