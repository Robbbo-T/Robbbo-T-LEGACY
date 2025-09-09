#!/usr/bin/env python3
"""
OEGI Genesis Artifact Validation Tool

EstándarUniversal: ArtefactoTecnico-Validacion-CAB-01.00-ValidadorOEGI-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHybrida-CROSS-AmedeoPelliccia-oegival1-RestoDeVidaUtil

Validates Genesis Artifacts against OEGI schema and business rules.
"""

import json
import yaml
import hashlib
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
import jsonschema
from typing import Dict, List, Any, Tuple

class OEGIValidator:
    """Validator for OEGI Genesis Artifacts"""
    
    def __init__(self, schema_path: str = None):
        if schema_path is None:
            schema_path = Path(__file__).parent.parent / "schemas" / "genesis-artifact.json"
        
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
            
        self.gi2_threshold = 0.6
        self.min_eligibility_checks = 3
        self.max_title_length = 200
        self.rights_duration_years = 8
    
    def validate_artifact(self, artifact_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a Genesis Artifact file
        Returns: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        try:
            # Load artifact
            with open(artifact_path, 'r', encoding='utf-8') as f:
                if artifact_path.endswith('.yaml') or artifact_path.endswith('.yml'):
                    artifact = yaml.safe_load(f)
                else:
                    artifact = json.load(f)
            
            # Schema validation
            try:
                jsonschema.validate(artifact, self.schema)
            except jsonschema.ValidationError as e:
                errors.append(f"Schema validation failed: {e.message}")
                return False, errors, warnings
            
            # Business rule validation
            record = artifact.get('oegi_record', {})
            
            # Validate OEGI ID format and sequence
            oegi_id = record.get('id', '')
            if not self._validate_oegi_id(oegi_id):
                errors.append(f"Invalid OEGI ID format: {oegi_id}")
            
            # Validate GI² score threshold
            gi2_score = record.get('eligibility', {}).get('gi2_score', 0)
            if gi2_score < self.gi2_threshold:
                errors.append(f"GI² score {gi2_score} below threshold {self.gi2_threshold}")
            
            # Validate eligibility checks
            checks_passed = record.get('eligibility', {}).get('checks_passed', [])
            if len(checks_passed) < self.min_eligibility_checks:
                errors.append(f"Only {len(checks_passed)} eligibility checks passed, minimum {self.min_eligibility_checks} required")
            
            # Validate timestamps
            timestamps = record.get('timestamps', {})
            timestamp_errors, timestamp_warnings = self._validate_timestamps(timestamps)
            errors.extend(timestamp_errors)
            warnings.extend(timestamp_warnings)
            
            # Validate hash format and length
            hashes = record.get('hashes', {})
            if 'sha256' in hashes:
                if not re.match(r'^[a-f0-9]{64}$', hashes['sha256']):
                    errors.append("SHA-256 hash format invalid")
            
            # Validate authors
            authors = record.get('authors', [])
            author_warnings = self._validate_authors(authors)
            warnings.extend(author_warnings)
            
            # Validate license compatibility
            license_type = record.get('license', '')
            license_warnings = self._validate_license(license_type)
            warnings.extend(license_warnings)
            
            # Check UTCS-MI header (if present in referenced content)
            utcs_warnings = self._check_utcs_mi_compliance(record)
            warnings.extend(utcs_warnings)
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        
        is_valid = len(errors) == 0
        return is_valid, errors, warnings
    
    def _validate_oegi_id(self, oegi_id: str) -> bool:
        """Validate OEGI ID format: OEGI-AG-YYYY-NNNNNN"""
        pattern = r'^OEGI-AG-\d{4}-\d{6}$'
        if not re.match(pattern, oegi_id):
            return False
        
        # Extract year and check reasonable range
        year = int(oegi_id[8:12])
        current_year = datetime.now().year
        if year < 2025 or year > current_year + 1:
            return False
            
        return True
    
    def _validate_timestamps(self, timestamps: Dict[str, str]) -> Tuple[List[str], List[str]]:
        """Validate timestamp formats and business rules"""
        errors = []
        warnings = []
        
        first_seen = timestamps.get('first_seen')
        certified_at = timestamps.get('certified_at')
        expires_at = timestamps.get('expires_at')
        
        # Parse timestamps
        try:
            if first_seen:
                first_dt = datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
                
            if certified_at:
                cert_dt = datetime.fromisoformat(certified_at.replace('Z', '+00:00'))
                
                # Check certification after first seen
                if first_seen and cert_dt < first_dt:
                    errors.append("Certification timestamp before first seen timestamp")
                    
                # Check certification not too far in future
                now = datetime.now(timezone.utc)
                if cert_dt > now + timedelta(days=1):
                    warnings.append("Certification timestamp appears to be in the future")
                    
            if expires_at:
                exp_dt = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                
                # Check expiration is ~8 years after certification
                if certified_at:
                    expected_exp = cert_dt + timedelta(days=8*365)
                    if abs((exp_dt - expected_exp).days) > 30:
                        warnings.append(f"Expiration date differs from expected 8-year duration")
                        
        except ValueError as e:
            errors.append(f"Invalid timestamp format: {e}")
        
        return errors, warnings
    
    def _validate_authors(self, authors: List[Dict[str, Any]]) -> List[str]:
        """Validate author information"""
        warnings = []
        
        for i, author in enumerate(authors):
            # Check ORCID format if provided
            orcid = author.get('orcid')
            if orcid and not re.match(r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$', orcid):
                warnings.append(f"Author {i+1}: Invalid ORCID format")
            
            # Recommend ORCID for attribution clarity
            if not orcid:
                warnings.append(f"Author {i+1}: ORCID recommended for clear attribution")
        
        return warnings
    
    def _validate_license(self, license_type: str) -> List[str]:
        """Validate license selection and compatibility"""
        warnings = []
        
        if license_type == 'GL-EU-BY-RF-1.0':
            warnings.append("GL-EU-BY-RF selected: Ensure FRAND tariff structure is configured")
        elif license_type == 'GL-EU-BY-RC-1.0':
            warnings.append("GL-EU-BY-RC selected: Ensure reciprocal sharing requirements are understood")
        
        return warnings
    
    def _check_utcs_mi_compliance(self, record: Dict[str, Any]) -> List[str]:
        """Check UTCS-MI compliance where applicable"""
        warnings = []
        
        # Check if title follows UTCS-MI patterns for technical artifacts
        title = record.get('title', '')
        if 'framework' in title.lower() or 'system' in title.lower():
            warnings.append("Technical artifact detected: consider UTCS-MI header compliance")
        
        return warnings

def main():
    """Main validation function"""
    if len(sys.argv) != 2:
        print("Usage: python validate_genesis_artifact.py <artifact_file>")
        sys.exit(1)
    
    artifact_path = sys.argv[1]
    
    if not Path(artifact_path).exists():
        print(f"Error: File {artifact_path} not found")
        sys.exit(1)
    
    validator = OEGIValidator()
    is_valid, errors, warnings = validator.validate_artifact(artifact_path)
    
    # Print results
    print(f"Validating: {artifact_path}")
    print("=" * 50)
    
    if errors:
        print("❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✅ Validation passed with no issues")
    elif not errors:
        print("✅ Validation passed with warnings")
    else:
        print("❌ Validation failed")
    
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()