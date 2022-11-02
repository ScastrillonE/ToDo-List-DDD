import rules
import exceptions

class BusinessRuleValidationMixin:
    def check_rules(self,rule:rules.BusinessRule):
        if rule.is_broken():
            raise exceptions.BusinessRuleValidationException(rule)