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
    """Select a random vowel symbol."""
    symbol = random.choice(list(vowel_data.keys()))
    return symbol, vowel_data[symbol]

def validate_selections(ipa_symbol, user_height, user_backness, user_rounding, user_tense_lax):
    """Check user's selections against the actual vowel properties."""
    correct_data = vowel_data[ipa_symbol]
    correct = (correct_data['Height'] == user_height and
               correct_data['Backness'] == user_backness and
               correct_data['Rounding'] == user_rounding and
               correct_data['Tense_Lax'] == user_tense_lax)
    return correct, correct_data

# Main interface with Streamlit
st.title("💧 Vowel Practice App")

# User name input
user_name = st.text_input("Enter your name:", value=st.session_state.get('user_name', ""))

# Start quiz button
if st.button("Start Quiz"):
    st.session_state.user_name = user_name
    st.session_state.correct_count = 0
    st.session_state.attempts = 0
    st.session_state.current_symbol, st.session_state.current_data = select_random_symbol()

if "current_symbol" in st.session_state:
    # Display the IPA Symbol along with its Name
    st.markdown(f"<h2>IPA Symbol: {st.session_state.current_symbol} ({st.session_state.current_data['Name']})</h2>", unsafe_allow_html=True)
    
    # Handling None values in session state to avoid index error
    height_default = st.session_state.get("user_height", "High") or "High"
    backness_default = st.session_state.get("user_backness", "Front") or "Front"
    rounding_default = st.session_state.get("user_rounding", "Unrounded") or "Unrounded"
    tense_lax_default = st.session_state.get("user_tense_lax", "Tense") or "Tense"
    
    # Display radio buttons with preserved selections
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        height = st.radio("Height", ['High', 'Mid', 'Low'], index=['High', 'Mid', 'Low'].index(height_default))
    with col2:
        backness = st.radio("Backness", ['Front', 'Central', 'Back'], index=['Front', 'Central', 'Back'].index(backness_default))
    with col3:
        rounding = st.radio("Rounding", ['Rounded', 'Unrounded'], index=['Rounded', 'Unrounded'].index(rounding_default))
    with col4:
        tense_lax = st.radio("Tense/Lax", ['Tense', 'Lax'], index=['Tense', 'Lax'].index(tense_lax_default))

    # Store current selections in session state to persist choices
    st.session_state.user_height = height
    st.session_state.user_backness = backness
    st.session_state.user_rounding = rounding
    st.session_state.user_tense_lax = tense_lax

    # Buttons for submission and continuation
    submit_pressed = st.button("Submit")
    continue_pressed = st.button("Show score & Continue")

    # Process submission
    if submit_pressed:
        correct, _ = validate_selections(st.session_state.current_symbol, height, backness, rounding, tense_lax)
        if correct:
            st.success("Correct!")
            st.session_state.correct_count += 1
        else:
            st.error("Incorrect!")
        st.session_state.attempts += 1

    # Show score and move to next symbol on "Show score & Continue"
    if continue_pressed:
        st.write(f"{st.session_state.user_name if 'user_name' in st.session_state else 'User'}'s score: {st.session_state.correct_count} out of {st.session_state.attempts}")
        # Update symbol for next question
        st.session_state.current_symbol, st.session_state.current_data = select_random_symbol()
        # Clear previous selections for the next question
        for key in ["user_height", "user_backness", "user_rounding", "user_tense_lax"]:
            st.session_state[key] = None  # Reset selections for the next question
