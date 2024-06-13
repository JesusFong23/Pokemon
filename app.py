import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Load the dataset
@st.cache_data  # Cache the dataset for better performance
def load_data():
    return pd.read_csv("Pokemon_with_images.csv")

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

                    # Calculate the total stats for each Pokémon
                    user_total_stats = user_pokemon_stats.sum()
                    opponent_total_stats = opponent_pokemon_stats.sum()

                    # Determine the winner based on total stats
                    st.write("Results:")
                    st.write(f"Your Pokémon: {user_pokemon['Name']}")
                    st.write(f"Opponent's Pokémon: {opponent_pokemon['Name'].values[0]}")
                    if user_total_stats > opponent_total_stats:
                        st.write("You win! 🎉")
                        st.image("https://media1.giphy.com/media/xx0JzzsBXzcMK542tx/giphy.gif?cid=6c09b952thbre9f6i9xkv790skz1sz5czdly9u2hh8n8nbx0&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g", width=200)
                    elif user_total_stats < opponent_total_stats:
                        st.write("You lose! 😢")
                        st.image("https://media1.giphy.com/media/dJYoOVAWf2QkU/giphy.gif?cid=6c09b952pifrrs3solvj7iq41nwhxf0vv5rsuwppptjn8ilz&ep=v1_gifs_search&rid=giphy.gif&ct=g", width=200)
                    else:
                        st.write("It's a tie! 🤝")

                    # Visualize the stats
                    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
                    stats_df = pd.DataFrame({'Stats': ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
                                             'Your Pokémon': user_pokemon_stats,
                                             "Opponent's Pokémon": opponent_pokemon_stats.flatten()})
                    stats_df.set_index('Stats', inplace=True)
                    stats_df.plot(kind='bar', ax=axes[0])
                    axes[0].set_ylabel('Stats')
                    axes[0].set_title('Comparison of Total Stats')

                    # Add text to explain the results
                    axes[1].axis('off')
                    axes[1].text(0.5, 0.5, "Your Total Stats: {}\nOpponent's Total Stats: {}".format(user_total_stats, opponent_total_stats),
                                 horizontalalignment='center', verticalalignment='center', fontsize=14)

                    st.pyplot(fig)

        st.markdown("<a href='?page=pikachu_game'>Go to Pikachu Mini Game</a>", unsafe_allow_html=True)

    elif page == 'pikachu_game':
        # Display Pikachu mini-game page
        pikachu_game()

        st.markdown("<a href='?page=main'>Go back to Pokémon Battle</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

