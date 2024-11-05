import streamlit as st
import random

# Vowel data from your CSV in dictionary format
vowel_data = {
    'i': {'Name': 'Lower case i', 'Height': 'High', 'Backness': 'Front', 'Rounding': 'Unrounded', 'Tense_Lax': 'Tense'},
    'ɪ': {'Name': 'Small capital i', 'Height': 'High', 'Backness': 'Front', 'Rounding': 'Unrounded', 'Tense_Lax': 'Lax'},
    'ɛ': {'Name': 'Epsilon', 'Height': 'Mid', 'Backness': 'Front', 'Rounding': 'Unrounded', 'Tense_Lax': 'Lax'},
    'æ': {'Name': 'Ash', 'Height': 'Low', 'Backness': 'Front', 'Rounding': 'Unrounded', 'Tense_Lax': 'Lax'},
    'u': {'Name': 'Lower case u', 'Height': 'High', 'Backness': 'Back', 'Rounding': 'Rounded', 'Tense_Lax': 'Tense'},
    'ʊ': {'Name': 'Small capital u', 'Height': 'High', 'Backness': 'Back', 'Rounding': 'Rounded', 'Tense_Lax': 'Lax'},
    'ɔ': {'Name': 'Open o', 'Height': 'Mid', 'Backness': 'Back', 'Rounding': 'Rounded', 'Tense_Lax': 'Tense'},
    'ɑ': {'Name': 'Back A', 'Height': 'Low', 'Backness': 'Back', 'Rounding': 'Unrounded', 'Tense_Lax': 'Tense'},
    'ɒ': {'Name': 'Turned back A', 'Height': 'Low', 'Backness': 'Back', 'Rounding': 'Rounded', 'Tense_Lax': 'Tense'},
    'ʌ': {'Name': 'Caret', 'Height': 'Mid', 'Backness': 'Central', 'Rounding': 'Unrounded', 'Tense_Lax': 'Lax'},
    'ə': {'Name': 'Schwa', 'Height': 'Mid', 'Backness': 'Central', 'Rounding': 'Unrounded', 'Tense_Lax': 'Lax'}
}

def select_random_symbol():
    """Select a random vowel symbol"""
    symbol = random.choice(list(vowel_data.keys()))
    return symbol, vowel_data[symbol]

def validate_selections(ipa_symbol, user_height, user_backness, user_rounding, user_tense_lax):
    """Check user's selections against the actual vowel properties"""
    correct_data = vowel_data[ipa_symbol]
    correct = (correct_data['Height'] == user_height and
               correct_data['Backness'] == user_backness and
               correct_data['Rounding'] == user_rounding and
               correct_data['Tense_Lax'] == user_tense_lax)
    
    return correct, correct_data

# Main interface with Streamlit
st.title("💧 Vowel Practice App")

# Textbox for user name input, always available
user_name = st.text_input("Enter your name:", value=st.session_state.user_name if 'user_name' in st.session_state else "")

# Start quiz button
if st.button("Start Quiz"):
    st.session_state.user_name = user_name
    st.session_state.correct_count = 0
    st.session_state.attempts = 0
    st.session_state.current_symbol, st.session_state.current_data = select_random_symbol()

if "current_symbol" in st.session_state:
    st.write(f"IPA Symbol: {st.session_state.current_symbol}")
    
    # Using columns to organize the options
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        height = st.radio("Height", ['High', 'Mid', 'Low'], key=f"height_{st.session_state.attempts}")
    with col2:
        backness = st.radio("Backness", ['Front', 'Central', 'Back'], key=f"backness_{st.session_state.attempts}")
    with col3:
        rounding = st.radio("Rounding", ['Rounded', 'Unrounded'], key=f"rounding_{st.session_state.attempts}")
    with col4:
        tense_lax = st.radio("Tense/Lax", ['Tense', 'Lax'], key=f"tense_lax_{st.session_state.attempts}")

    # Place buttons next to each other without any gap
    cols = st.columns([2, 3, 5])  # Adjust the width of the first two columns to bring buttons closer
    with cols[0]:
        submit_pressed = st.button("Submit")
    with cols[1]:
        continue_pressed = st.button("Show score & Continue")

    # Process the submission and update
    if submit_pressed:
        correct, _ = validate_selections(st.session_state.current_symbol, height, backness, rounding, tense_lax)
        if correct:
            st.success("Correct!")
            st.session_state.correct_count += 1
        else:
            st.error("Incorrect!")
        st.session_state.attempts += 1
        st.session_state.current_symbol, st.session_state.current_data = select_random_symbol()

    # Show score when 'Continue' is pressed
    if continue_pressed:
        st.write(f"{st.session_state.user_name if 'user_name' in st.session_state else 'User'} score: {st.session_state.correct_count} out of {st.session_state.attempts}")
