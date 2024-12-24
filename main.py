from i_questionnaire_engine import run_questionnaire_engine
from ii_diagnosis_engine import run_diagnosis_engine
from iii_airway_assessment import run_airway_assessment
from iv_symptom_assessment import run_symptom_assessment

if __name__ == "__main__":
    if run_questionnaire_engine():
      if run_diagnosis_engine():
         run_airway_assessment()
         run_symptom_assessment()