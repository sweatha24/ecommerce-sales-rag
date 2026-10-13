from pymongo import MongoClient

class SalesAnalytics:
    def __init__(self, db):
        self.sales_col = db['sales']

    def aggregate_store_kpis(self):
        """Aggregates sales performance by store using PyMongo pipelines."""
        pipeline = [
            {"$unwind": "$items"},
            {
                "$group": {
                    "_id": "$store_id",
                    "total_revenue": {"$sum": "$total_amount"},
                    "total_orders": {"$addToSet": "$order_id"},
                    "total_items_sold": {"$sum": "$items.quantity"},
                    "avg_order_value": {"$avg": "$total_amount"}
                }
            },
            {
                "$project": {
                    "store_id": "$_id",
                    "_id": 0,
                    "total_revenue": {"$round": ["$total_revenue", 2]},
                    "total_orders_count": {"$size": "$total_orders"},
                    "total_items_sold": 1,
                    "avg_order_value": {"$round": ["$avg_order_value", 2]}
                }
            },
            {"$sort": {"total_revenue": -1}}
        ]
        
        return list(self.sales_col.aggregate(pipeline))

    def generate_store_summary_text(self):
        """Transforms KPI metrics into textual context for vector embedding."""
        kpis = self.aggregate_store_kpis()
        documents = []
        
        for kpi in kpis:
            text_summary = (
                f"Store ID {kpi['store_id']} achieved a total revenue of ${kpi['total_revenue']} "
                f"across {kpi['total_orders_count']} orders. Total items sold: {kpi['total_items_sold']}. "
                f"The average order value was ${kpi['avg_order_value']}."
            )
            documents.append({
                "store_id": kpi['store_id'],
                "summary": text_summary,
                "type": "store_kpi_summary"
            })
        return documents