import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Create a login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Pokemon" and password == "Pokemon123":
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password")

# Load the dataset
@st.cache_data()  # Cache the dataset for better performance
def load_data():
    return pd.read_csv("Pokemon_with_images.csv")

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

    # Display opponent's Pokémon
    if "opponent_pokemon" not in st.session_state:
        st.session_state.opponent_pokemon = df.sample(n=1)
    opponent_pokemon = st.session_state.opponent_pokemon
    st.write("Opponent's Pokémon:")
    st.image(opponent_pokemon['Image URL'].values[0], width=200)
    st.write(opponent_pokemon[['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']])

    # Reset button
    if st.button("Reset"):
        st.session_state.opponent_pokemon = df.sample(n=1)
        st.experimental_rerun()

    # Select the user's Pokémon
    st.write("Choose your Pokémon:")
    user_pokemon_name = st.selectbox("Select your Pokémon", [""] + df['Name'].tolist())

    if user_pokemon_name:
        user_pokemon = df[df['Name'] == user_pokemon_name]
        st.image(user_pokemon['Image URL'].values[0], width=200)

    # Fight button centered
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if user_pokemon_name != "" and st.button("Fight"):
            if user_pokemon.empty:
                st.write("Sorry, that Pokémon is not found in the dataset.")
            else:
                # Get the stats of user's and opponent's Pokémon
                user_pokemon_stats = user_pokemon[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values[0]
                opponent_pokemon_stats = opponent_pokemon[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values[0]

                # Calculate the total stats for each Pokémon
                user_total_stats = sum(user_pokemon_stats)
                opponent_total_stats = sum(opponent_pokemon_stats)

                # Determine the winner based on total stats
                st.write("Results:")
                st.write(f"Your Pokémon: {user_pokemon_name}")
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
                                         "Opponent's Pokémon": opponent_pokemon_stats})
                stats_df.set_index('Stats', inplace=True)
                stats_df.plot(kind='bar', ax=axes[0])
                axes[0].set_ylabel('Stats')
                axes[0].set_title('Comparison of Total Stats')

                # Add text to explain the results
                axes[1].axis('off')
                axes[1].text(0.5, 0.5, "Your Total Stats: {}\nOpponent's Total Stats: {}".format(user_total_stats, opponent_total_stats),
                             horizontalalignment='center', verticalalignment='center', fontsize=14)

                st.pyplot(fig)

if __name__ == "__main__":
    main()



