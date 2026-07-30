import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('balance_validator',ROOT/'scripts/validate_balance_model.py')

class BalanceModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(cls.mod)

    def valid_model(self):
        return {
            'target_experience':'新手可理解失败原因，熟练玩家仍需改变策略而非只提高数值',
            'skill_bands':['novice','competent','expert'],
            'challenge_dimensions':['information','decision','execution','resource'],
            'metrics':[{'id':'completion_rate','target_min':0.45,'target_max':0.75,'segment':'competent'}],
            'tuning_parameters':[{'id':'enemy_spawn_budget','min':2,'max':12,'default':6,'step':1}],
            'difficulty_curve':[{'stage':1,'challenge_budget':3},{'stage':2,'challenge_budget':5},{'stage':3,'challenge_budget':8}],
            'adaptation_policy':{'enabled':True,'signals':['recent_failures'],'allowed_adjustments':['support_drop','spawn_frequency'],'cooldown_s':45,'max_step':1,'player_respect':'不修改已学习的敌人攻击规则'},
            'playtest_hypotheses':[{'hypothesis':'中等玩家第三关完成率在目标区间','measure':'completion_rate','falsifier':'低于0.45或高于0.75'}]
        }

    def test_valid_model_passes(self):
        self.assertEqual(self.mod.validate(self.valid_model())['errors'],[])

    def test_invalid_parameter_bounds_fail(self):
        model=self.valid_model(); model['tuning_parameters'][0]['default']=20
        result=self.mod.validate(model)
        self.assertTrue(any('outside bounds' in e for e in result['errors']))

    def test_adaptation_without_cooldown_fails(self):
        model=self.valid_model(); del model['adaptation_policy']['cooldown_s']
        result=self.mod.validate(model)
        self.assertTrue(any('cooldown' in e for e in result['errors']))
