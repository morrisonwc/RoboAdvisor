import pandas as pd
from dateutil import parser, relativedelta
from datetime import date

class Goal:
    def __init__(self, name, targetYear, targetValue, initialContribution=0, monthlyContribution=0, priority=""):
        self.name = name
        self.targetYear = targetYear
        self.targetValue = targetValue
        self.initialContribution = initialContribution
        self.monthlyContribution = monthlyContribution
        if not (priority == "") and not (priority in ["Dreams", "Wishes", "Wants", "Needs"]):
            raise ValueError("Wrong value set for Priority.")
        self.priority = priority
    
    def get_goal_probabilities(self):
        if (self.priority == ""):
            raise ValueError("No value set for Priority")
        #### Change path before use ####
        lookupTable = pd.read_csv("Goal Probability Table.csv")
        match = (lookupTable["Realize"] == self.priority)
        minProb = lookupTable["MinP"][(match)]
        maxProb = lookupTable["MaxP"][(match)]
        return minProb.values[0], maxProb.values[0]
    
    def check_goal_plausible(df: pd.DataFrame, goalValue) -> bool:
        maxValue = df["value"].max()
        if maxValue >= goalValue:
            return True
        else:
            return False
        

class RetirementGoal(Goal):
    def __init__(self, name, targetValue, startingAge, retirementAge):
        targetYear = date.today().year + (retirementAge-startingAge)
        super().__init__(name, targetYear, targetValue)
        self.retirementAge = retirementAge


class GrowWealthGoal(Goal):
    def __init__(self, initialContribution, monthlyContribution):
        targetYear = date.today().year + 10
        targetAmount = 1000000
        super().__init__("Grow My Wealth", targetYear, targetAmount, initialContribution, monthlyContribution)


class EducationGoal(Goal):
    def __init__(self, name, startYear, degreeLengthYears, annualTuitionFees, degreeType, schoolName):
        targetValue = degreeLengthYears * annualTuitionFees
        super().__init__(name, startYear, targetValue)
        self.degreeType = degreeType
        self.schoolName = schoolName


class RealEstateGoal(Goal):
    def __init__(self, name, targetYear, homeValue, downPayment, mortgagePayment, interestRate):
        targetValue = downPayment
        super().__init__(name, targetYear, targetValue)
        self.homeValue = homeValue
        self.mortgagePayment = mortgagePayment
        self.interestRate = interestRate


class StartupGoal(Goal):
    def __init__(self, companyName, startYear, seedFunding):
        super().__init__(companyName, startYear, seedFunding)


class SavingsGoal:
    def __init__(self, name, targetDate, targetValue, initialContribution, monthlyContribution):
        targetDateTime = parser.parse(targetDate)
        delta = relativedelta(targetDateTime, date.today())
        difference_in_months = delta.months + delta.years * 12
        value = initialContribution + (monthlyContribution * difference_in_months)
        print(value)

        if not (value >= targetValue):
            raise ValueError("Target value too hight to be achieved.")
        
        self.name = name
        self.targetDate = targetDate
        self.targetValue = targetValue
        self.initialContribution = initialContribution
        self.monthlyContribution = monthlyContribution


class WeddingGoal(SavingsGoal):
    def __init__(self, name, weddingDate, budget, initialContribution, monthlyContribution):
        super().__init__(name, weddingDate, budget, initialContribution, monthlyContribution)
        self.weddingDate = weddingDate


class TravelGoal(SavingsGoal):
    def __init__(self, destination, tripDate, tripDuration, budget, initialContribution, monthlyContribution):
        super().__init__(destination, tripDate, budget, initialContribution, monthlyContribution)
        self.tripDuration = tripDuration


class SplurgeGoal(SavingsGoal):
    def __init__(self, itemName, storeName, targetPurchaseDate, budget, initialContribution, monthlyContribution):
        super().__init__(itemName + " @ " + storeName, targetPurchaseDate, budget, initialContribution, monthlyContribution)


class IncomeGoal:
    def __init__(self, durationYears, startingValue, monthlyDividend):
        self.durationYears = durationYears
        self.startingValue = startingValue
        self.monthlyDividend = monthlyDividend


class RetirementIncome(IncomeGoal):
    def __init__(self, retirementSavings, currentAge, retirementAge, retirementIncome):
        lifeExpectancy = 79
        durationYears = lifeExpectancy - retirementAge
        super().__init__(durationYears, retirementSavings, retirementIncome)
        self.retirementYear = date.today().year + (retirementAge - currentAge)
