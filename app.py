import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Disable deprecated warning for st.pyplot() usage
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load the RandomForestClassifier model
model_path = "pokemon_rf_model.pkl"  # Update to point directly to the model file
rf_classifier = joblib.load(model_path)

# Create a login page with instructions and an image
def login():
    st.title("Welcome to Pokémon Battle!")
    
    # Add the image to the login page
    st.image("https://4kwallpapers.com/images/walls/thumbs_2t/16032.jpg", use_column_width=True)
    
    st.write("### How to Play:")
    st.write("1. 🆚 **View the Opponent:** See which Pokémon you're up against.")
    st.write("2. 🔍 **Choose Your Pokémon:** Pick one of the five random Pokémon.")
    st.write("3. 📊 **Check the Stats:** Compare your Pokémon's stats with your opponent's.")
    st.write("4. ⚔️ **Fight!**: Click the Fight button and see who wins!")
    st.write("Good luck, Trainer! 🍀")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Pokemon" and password == "Pokemon123":
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password")

# Load the dataset using st.cache
@st.cache  # Cache the dataset for better performance
def load_data():
    return pd.read_csv("Pokemon_with_images.csv")  # Assumes Pokemon_with_images.csv is in the same directory as app.py

# Pikachu mini-game page
def pikachu_game():
    st.title("Pikachu Mini Game")
    st.write("Welcome to Pikachu's world!")
    
    st.image("https://i.gifer.com/Td9n.gif", width=300)
    
    st.write("Here you can interact with Pikachu:")
    interaction = st.radio("Select an action:", ["Feed", "Play", "Sleep", "Compliment"])

    # Handle interaction actions
    if interaction == "Feed":
        st.image("https://media4.giphy.com/media/ukpwkOzk6kafXwfwbH/giphy.gif?cid=6c09b952akhgixuezhxzuxnb37w2s7z9yh30767jjktom21n&ep=v1_gifs_search&rid=giphy.gif&ct=g", width=200)
        st.write("You fed Pikachu!")

    elif interaction == "Play":
        st.image("https://i.gifer.com/N8J.gif", width=200)
        st.write("You played with Pikachu!")

    elif interaction == "Sleep":
        st.image("https://media4.giphy.com/media/iK4rg28Vg3A6Q/giphy.gif?cid=6c09b952p8pk3g3q07vj4uw29sh4lgv0mbpeb96m51a0lrfk&ep=v1_gifs_search&rid=giphy.gif&ct=g", width=200)
        st.write("Pikachu is sleeping Zzz...")

    elif interaction == "Compliment":
        st.image("https://i.pinimg.com/originals/ba/32/10/ba321060bf6e28126654667bbebfcf74.gif", width=200)
        st.write("You complimented Pikachu! Pikachu is happy!")

# Main function
def main():
    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Authenticate user
    if not st.session_state.logged_in:
        login()
        return

    # Load the dataset
    df = load_data()

    # Reset functionality to refresh opponent's Pokémon and user's options
    if "opponent_pokemon" not in st.session_state or st.button("Reset"):
        st.session_state.opponent_pokemon = df.sample(n=1)
        st.session_state.user_pokemon_choices = df.sample(n=5)
        if "user_pokemon" in st.session_state:
            del st.session_state["user_pokemon"]

    # Handle navigation between main game and Pikachu mini-game
    page = st.query_params.get('page', 'main')

    if page == 'main':
        # Display main game content
        st.title("Pokémon Battle!")

        # Display opponent's Pokémon
        opponent_pokemon = st.session_state.opponent_pokemon
        st.write("Opponent's Pokémon:")
        st.image(opponent_pokemon['Image URL'].values[0], width=200)
        st.write(opponent_pokemon[['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']])

        st.write("Choose your Pokémon:")
        user_pokemon_choices = st.session_state.user_pokemon_choices

        col1, col2, col3, col4, col5 = st.columns(5)
        for idx, col in enumerate([col1, col2, col3, col4, col5]):
            pokemon = user_pokemon_choices.iloc[idx]
            if col.button(pokemon['Name']):
                st.session_state.user_pokemon = pokemon

        if "user_pokemon" in st.session_state:
            user_pokemon = st.session_state.user_pokemon
            st.image(user_pokemon['Image URL'], width=200)
            st.write(user_pokemon[['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']])

            # Fight button centered
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Fight"):
                    # Get the stats of user's and opponent's Pokémon
                    user_pokemon_stats = user_pokemon[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.flatten()
                    opponent_pokemon_stats = opponent_pokemon[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.flatten()

                    # Predict the winner using RandomForestClassifier
                    user_stats_for_prediction = user_pokemon_stats.reshape(1, -1)
                    opponent_stats_for_prediction = opponent_pokemon_stats.reshape(1, -1)

                    user_prediction = rf_classifier.predict(user_stats_for_prediction)[0]
                    opponent_prediction = rf_classifier.predict(opponent_stats_for_prediction)[0]

                    if user_prediction == 1:
                        user_predicted_winner = "You win! 🎉"
                    else:
                        user_predicted_winner = "You lose! 😢"

                    st.write("Results:")
                    st.write(f"Your Pokémon: {user_pokemon['Name']}")
                    st.write(f"Opponent's Pokémon: {opponent_pokemon['Name'].values[0]}")
                    st.write(f"Predicted Winner: {user_predicted_winner}")

                    # Display appropriate gif based on prediction
                    if user_prediction == 1:
                        st.image("https://media1.giphy.com/media/xx0JzzsBXzcMK542tx/giphy.gif?cid=6c09b952thbre9f6i9xkv790skz1sz5czdly9u2hh8n8nbx0&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g", width=200)
                    else:
                        st.image("https://media1.giphy.com/media/dJYoOVAWf2QkU/giphy.gif?cid=6c09b952pifrrs3solvj7iq41nwhxf0vv5rsuwppptjn8ilz&ep=v1_gifs_search&rid=giphy.gif&ct=g", width=200)

                    # Show why the Pokémon won or lost
                    st.write("Comparison of Stats:")
                    
                    # Prepare stats data for plotting
                    stats_df = pd.DataFrame({
                        'Stats': ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
                        user_pokemon['Name']: user_pokemon_stats,
                        opponent_pokemon['Name'].values[0]: opponent_pokemon_stats
                    })

                    # Melt the DataFrame for Seaborn barplot
                    stats_df_melted = stats_df.melt(id_vars='Stats', var_name='Pokemon', value_name='Value')

                    # Plot using Seaborn barplot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(x='Stats', y)                    # Plot using Seaborn barplot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(x='Stats', y='Value', hue='Pokemon', data=stats_df_melted, palette='viridis', ax=ax)
                    ax.set_title("Comparison of Pokémon Stats")
                    ax.set_xlabel("Stats")
                    ax.set_ylabel("Value")
                    ax.legend(title='Pokemon')

                    # Display the plot using Streamlit
                    st.pyplot(fig)

                    # Add a link to Pikachu's mini-game
                    st.markdown("<a href='?page=pikachu'>Play Pikachu's Mini-Game</a>", unsafe_allow_html=True)

        else:
            st.write("Please choose your Pokémon to start the battle.")

    elif page == 'pikachu':
        pikachu_game()
        st.markdown("<a href='?page=main'>Back to Main Game</a>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()


