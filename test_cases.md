# Flask User Profile Manager - Test Cases Documentation

## Test Case 1: Valid User Registration (Positive Test)
**Test Type:** Valid Input Test  
**Purpose:** Verify that valid user data is successfully registered  
**Test Data:**
- First Name: "John"
- Last Name: "Doe"  
- Email: "john.doe@example.com"
- Age: 25
- Bio: "Software developer with 5 years experience"

**Expected Result:** 
- User successfully registered
- Redirect to home page
- Success message displayed
- User appears in user list

**Test Steps:**
1. Navigate to `/register`
2. Fill form with valid data
3. Submit form
4. Verify redirect to home page
5. Check user appears in list

---

## Test Case 2: Invalid Email Format (Negative Test)
**Test Type:** Invalid Input Test  
**Purpose:** Verify email validation works correctly  
**Test Data:**
- First Name: "Jane"
- Last Name: "Smith"
- Email: "invalid-email" (no @ symbol)
- Age: 30
- Bio: "Marketing specialist"

**Expected Result:**
- Form validation error displayed
- "Please enter a valid email address" message shown
- User not registered
- Form remains on registration page

**Test Steps:**
1. Navigate to `/register`
2. Fill form with invalid email
3. Submit form
4. Verify error message appears
5. Confirm user not created

---

## Test Case 3: Age Boundary Testing (Edge Case)
**Test Type:** Boundary Value Test  
**Purpose:** Test age validation boundaries  
**Test Data Sets:**
- Set A: Age = 12 (below minimum)
- Set B: Age = 13 (minimum valid)
- Set C: Age = 120 (maximum valid)
- Set D: Age = 121 (above maximum)

**Expected Results:**
- Age 12: Validation error "Age must be between 13 and 120"
- Age 13: Successful registration
- Age 120: Successful registration  
- Age 121: Validation error "Age must be between 13 and 120"

**Test Steps:**
1. Test each age value in separate registration attempts
2. Verify validation messages for invalid ages
3. Verify successful registration for valid ages

---

## Test Case 4: Duplicate Email Registration (Business Logic Test)
**Test Type:** Duplicate Data Test  
**Purpose:** Verify duplicate email handling  
**Test Data:**
- Register first user with email "test@example.com"
- Attempt to register second user with same email

**Expected Result:**
- First registration: Success
- Second registration: Error message "Email address already exists"
- Only one user record created

**Test Steps:**
1. Register first user successfully
2. Attempt to register second user with same email
3. Verify error message displayed
4. Confirm only one user in database

---

## Test Case 5: Empty Required Fields (Validation Test)
**Test Type:** Required Field Test  
**Purpose:** Verify required field validation  
**Test Data:**
- First Name: "" (empty)
- Last Name: "" (empty)
- Email: "" (empty)
- Age: "" (empty)
- Bio: "Optional field content"

**Expected Result:**
- Multiple validation errors displayed:
  - "First name is required"
  - "Last name is required"
  - "Email is required"
  - "Age is required"
- Form not submitted
- User not registered

**Test Steps:**
1. Navigate to `/register`
2. Leave required fields empty
3. Submit form
4. Verify all validation errors appear
5. Confirm no user created

---

## Test Case 6: Bio Length Validation (Edge Case)
**Test Type:** Field Length Test  
**Purpose:** Test bio field length limits  
**Test Data:**
- Valid data for all required fields
- Bio: 501 characters (exceeds 500 limit)

**Expected Result:**
- Validation error: "Bio must be less than 500 characters"
- Form not submitted
- User not registered

**Test Steps:**
1. Fill form with valid data
2. Enter 501 character bio
3. Submit form
4. Verify length validation error
5. Confirm user not created

---

## Test Case 7: Profile Update with Pre-loaded Data (Functional Test)
**Test Type:** Update Functionality Test  
**Purpose:** Verify profile update works correctly  
**Test Data:**
- Create user first
- Update email to "updated@example.com"
- Update age to 35

**Expected Result:**
- Update form pre-populated with existing data
- Changes saved successfully
- Updated data displayed in profile
- Success message shown

**Test Steps:**
1. Create a user
2. Navigate to update profile
3. Verify form pre-populated
4. Make changes and submit
5. Verify changes saved and displayed

---

## Test Case 8: Non-existent User Profile Access (Error Handling Test)
**Test Type:** Error Handling Test  
**Purpose:** Test handling of invalid user IDs  
**Test Data:**
- Navigate to `/profile/999` (non-existent ID)
- Navigate to `/update/999` (non-existent ID)

**Expected Result:**
- Error message: "User not found"
- Redirect to home page
- No application crash

**Test Steps:**
1. Navigate to invalid profile URL
2. Verify error handling
3. Confirm redirect to home
4. Test with update URL too

---

## Test Case 9: Name Length Validation (Boundary Test)
**Test Type:** Field Length Boundary Test  
**Purpose:** Test name field length limits  
**Test Data:**
- First Name: "A" (1 character - below minimum)
- Last Name: "AB" (2 characters - minimum valid)
- First Name: 51 characters (above maximum)

**Expected Result:**
- 1 character: "First name must be between 2 and 50 characters"
- 2 characters: Success
- 51 characters: "First name must be between 2 and 50 characters"

**Test Steps:**
1. Test each boundary value
2. Verify validation messages
3. Confirm valid lengths work

---

## Test Case 10: SQL Injection Prevention (Security Test)
**Test Type:** Security Test  
**Purpose:** Verify SQL injection protection  
**Test Data:**
- Email: "test@example.com'; DROP TABLE users; --"
- First Name: "'; DELETE FROM users; --"

**Expected Result:**
- Input treated as literal text
- No SQL commands executed
- Normal validation applied
- Database remains intact

**Test Steps:**
1. Enter SQL injection attempts
2. Submit form
3. Verify database not affected
4. Confirm input sanitized

---

## Test Execution Summary Template

| Test Case | Status | Notes | Screenshot |
|-----------|--------|-------|------------|
| 1. Valid Registration | PASS/FAIL | | |
| 2. Invalid Email | PASS/FAIL | | |
| 3. Age Boundaries | PASS/FAIL | | |
| 4. Duplicate Email | PASS/FAIL | | |
| 5. Empty Required Fields | PASS/FAIL | | |
| 6. Bio Length | PASS/FAIL | | |
| 7. Profile Update | PASS/FAIL | | |
| 8. Non-existent User | PASS/FAIL | | |
| 9. Name Length | PASS/FAIL | | |
| 10. SQL Injection | PASS/FAIL | | |

## Testing Environment
- **Application:** Flask User Profile Manager
- **Python Version:** 3.12
- **Flask Version:** 2.3.3
- **Database:** SQLite
- **Browser:** Chrome/Firefox/Edge
- **Operating System:** Windows 10

## Test Data Files
- Valid test users data
- Invalid input samples
- Edge case scenarios
- Security test payloads 