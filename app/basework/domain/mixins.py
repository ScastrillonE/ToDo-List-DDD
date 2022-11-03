from app.basework.domain import rules,exceptions

class BusinessRuleValidationMixin:
    def check_rules(self,rule:rules.BusinessRule):
        if rule.is_broken():
            raise exceptions.BusinessRuleValidationException(rule)