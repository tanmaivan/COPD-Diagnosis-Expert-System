from questionnaire_engine import run_questionnaire_engine
from diagnosis_engine import run_diagnosis_engine
from airway_assessment import run_airway_assessment
from symptom_assessment import run_symptom_assessment

if __name__ == "__main__":
    if run_questionnaire_engine():
      run_diagnosis_engine()
      run_airway_assessment()
      run_symptom_assessment()