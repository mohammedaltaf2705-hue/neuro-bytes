from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class BloodType(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "unknown"


class PatientInfo(BaseModel):
    """Patient demographic and identification information"""
    patient_id: Optional[str] = Field(None, description="Patient ID or MRN")
    first_name: Optional[str] = Field(None, description="Patient first name")
    last_name: Optional[str] = Field(None, description="Patient last name")
    full_name: Optional[str] = Field(None, description="Patient full name")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age")
    gender: Optional[Gender] = Field(None, description="Patient gender")
    blood_type: Optional[BloodType] = Field(None, description="Blood type")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[str] = Field(None, description="Contact email")
    address: Optional[str] = Field(None, description="Patient address")
    
    class Config:
        use_enum_values = True


class VitalSigns(BaseModel):
    """Patient vital signs measurements"""
    temperature: Optional[float] = Field(None, description="Body temperature in Fahrenheit")
    temperature_celsius: Optional[float] = Field(None, description="Body temperature in Celsius")
    blood_pressure_systolic: Optional[int] = Field(None, description="Systolic BP (mmHg)")
    blood_pressure_diastolic: Optional[int] = Field(None, description="Diastolic BP (mmHg)")
    heart_rate: Optional[int] = Field(None, description="Heart rate (bpm)")
    respiratory_rate: Optional[int] = Field(None, description="Respiratory rate (breaths/min)")
    oxygen_saturation: Optional[float] = Field(None, ge=0, le=100, description="SpO2 (%)")
    weight: Optional[float] = Field(None, description="Weight in pounds")
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    height: Optional[float] = Field(None, description="Height in inches")
    height_cm: Optional[float] = Field(None, description="Height in centimeters")
    bmi: Optional[float] = Field(None, description="Body Mass Index")
    recorded_date: Optional[datetime] = Field(None, description="When vitals were recorded")


class LabResult(BaseModel):
    """Laboratory test results"""
    test_name: str = Field(..., description="Name of the lab test")
    value: Optional[str] = Field(None, description="Test result value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    reference_range: Optional[str] = Field(None, description="Normal reference range")
    status: Optional[str] = Field(None, description="Result status (normal, abnormal, critical)")
    test_date: Optional[date] = Field(None, description="Date test was performed")
    notes: Optional[str] = Field(None, description="Additional notes")


class Medication(BaseModel):
    """Medication information"""
    name: str = Field(..., description="Medication name")
    dosage: Optional[str] = Field(None, description="Dosage amount")
    frequency: Optional[str] = Field(None, description="Frequency of administration")
    route: Optional[str] = Field(None, description="Route of administration")
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date")
    prescribing_doctor: Optional[str] = Field(None, description="Prescribing physician")
    indication: Optional[str] = Field(None, description="Reason for medication")
    notes: Optional[str] = Field(None, description="Additional notes")


class Diagnosis(BaseModel):
    """Medical diagnosis information"""
    condition: str = Field(..., description="Diagnosis or condition name")
    icd_code: Optional[str] = Field(None, description="ICD-10 or ICD-9 code")
    diagnosis_date: Optional[date] = Field(None, description="Date of diagnosis")
    status: Optional[str] = Field(None, description="Status (active, resolved, chronic)")
    severity: Optional[str] = Field(None, description="Severity level")
    notes: Optional[str] = Field(None, description="Additional notes")


class MedicalHistory(BaseModel):
    """Patient medical history"""
    allergies: List[str] = Field(default_factory=list, description="Known allergies")
    chronic_conditions: List[str] = Field(default_factory=list, description="Chronic conditions")
    past_surgeries: List[str] = Field(default_factory=list, description="Past surgical procedures")
    family_history: List[str] = Field(default_factory=list, description="Family medical history")
    social_history: Optional[str] = Field(None, description="Social history (smoking, alcohol, etc.)")
    immunizations: List[str] = Field(default_factory=list, description="Immunization history")


class MedicalRecord(BaseModel):
    """Complete medical record structure"""
    patient_info: Optional[PatientInfo] = Field(None, description="Patient information")
    vital_signs: Optional[VitalSigns] = Field(None, description="Vital signs")
    lab_results: List[LabResult] = Field(default_factory=list, description="Laboratory results")
    medications: List[Medication] = Field(default_factory=list, description="Current medications")
    diagnoses: List[Diagnosis] = Field(default_factory=list, description="Diagnoses")
    medical_history: Optional[MedicalHistory] = Field(None, description="Medical history")
    visit_date: Optional[datetime] = Field(None, description="Visit or record date")
    provider: Optional[str] = Field(None, description="Healthcare provider")
    facility: Optional[str] = Field(None, description="Healthcare facility")
    notes: Optional[str] = Field(None, description="Additional clinical notes")


class ExtractionResult(BaseModel):
    """Result of medical data extraction"""
    success: bool = Field(..., description="Whether extraction was successful")
    medical_record: Optional[MedicalRecord] = Field(None, description="Extracted medical record")
    raw_text: Optional[str] = Field(None, description="Raw extracted text")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="Confidence score")
    extraction_method: Optional[str] = Field(None, description="Method used for extraction")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    warnings: List[str] = Field(default_factory=list, description="Any warnings")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
