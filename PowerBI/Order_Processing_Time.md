# Tracking Sales Order Processing Time with Power BI

Understanding how quickly sales orders is processed. 
This Power BI project transforms order data into actionable insights that reveal bottlenecks and improvement opportunities.

## The Business Challenge

Sales teams and operations managers need answers to critical questions:
- How long does it take from order placement to fulfillment?
- Where are the bottlenecks in our order process?
- How is the carrier's performance?

## Project Overview

This Power BI dashboard tracks orders through multiple stages and calculates key processing metrics:

**Key Metrics:**
- Handling Time: from receive an order to dispatch at warehouse
- Ship-to-Delivery Time  
- Total Order Cycle Time
- On-time delivery rates
- Processing time by product category and customer segment

## Data Model

The solution connects Orders, Products, Customers, and Calendar tables. Key DAX measures include:

```dax
Avg Order Processing Days = 
AVERAGE(
    DATEDIFF(Orders[OrderDate], Orders[ShipDate], DAY)
)

On-Time Delivery Rate = 
DIVIDE(
    COUNTROWS(FILTER(Orders, Orders[ActualDelivery] <= Orders[PromisedDelivery])),
    COUNTROWS(Orders)
) * 100
```

## Dashboard Design

The multi-page dashboard includes:
- **Executive Summary:** High-level KPIs and trends

<img width="710" alt="sale_order_01" src="https://github.com/user-attachments/assets/f403ec99-f28b-4665-a1de-c9a7774dd8a2" />
  
- **Operations Dashboard:** Real-time monitoring per customers

<img width="704" alt="sale_order_02" src="https://github.com/user-attachments/assets/51e3a2c0-2ac4-41d4-b54b-9440a02a780d" />


## Business Impact

The dashboard delivered measurable results:
- Reduced average processing time by 18%
- Improved on-time delivery from 87% to 94%
- Reduced shipping costs by 12% through optimized fulfillment
