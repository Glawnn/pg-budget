from datetime import datetime
from pg_budget.core.models.expense import Expense
from pg_budget.core.services.crud_services import CRUDService

class ExpenseService(CRUDService):
    def __init__(self):
        super().__init__(Expense)

    def get_by_category(self, category_id):
        all_expenses = self.get_all()
        return [Expense(**expense) for expense in all_expenses if expense['category_id'] == category_id]
    
    def get_by_plan(self, plan_id):
        all_expenses = self.get_all()
        return [Expense(**expense) for expense in all_expenses if expense['plan_id'] == plan_id]
    
    def mark_as_payed(self, expense_id):
        all_expenses = self.get_all()
        for expense in all_expenses:
            if expense['expense_id'] == expense_id:
                expense['payed'] = True
                self.update(expense_id, expense)
                return Expense(**expense)
            
    def mark_as_unpayed(self, expense_id):
        all_expenses = self.get_all()
        for expense in all_expenses:
            if expense['expense_id'] == expense_id:
                expense['payed'] = False
                self.update(expense_id, expense)
                return Expense(**expense)
    
    def get_by_month(self, year: int, month: int):
        all_expenses = self.get_all()
        filtered_expenses = []
        for expense in all_expenses:
            date = datetime.strptime(expense['date'], "%Y-%m-%d")
            if date.year == year and date.month == month:
                filtered_expenses.append(Expense(**expense))
        return filtered_expenses
    

expenseService = ExpenseService()