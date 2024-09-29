<img
    src="./images/banner.png"
    alt="Collide Banner"
    width="100%"
/>

<hr>

# Collide Content Recommendation Engine

### About

This project was created for the [2024 Collide Hackathon](https://lu.ma/bj69zi5z?tk=1greLq) hosted by [Digital Wildcatters](https://digitalwildcatters.com). Not only did we win **1st place**, but we also won the **Most Creative** and **Best UI/UX** awards, and our team was awarded **$1,750** in prize money!

- View our Devpost submission [here](https://devpost.com/software/collide-content-recommendation-engine?ref_content=user-portfolio&ref_feature=in_progress).
- See our project presentation and demo [here](#). [TODO]

### Chosen Prompt

#### Prompt 1a

> ​Create a content ranking engine for Collide. Data includes posts, comments, fake user profiles.

#### Prompt Explanation

Users on [Collide](https://collide.io) need recommendations. The for this challenege is to **create a recommendation engine** that shows a user posts and content tailored to their role and interests.

- Use the data from the user profiles, comments, likes/dislikes table to create a a summary statement about the user.
- We can use this to add context to a system prompts in Collide.
- Follow recommendations based on location/interests/engagement.
- This will be a discovery mechanism for Collide.

### Screenshots

<img
    src="./images/feed.png"
    alt="Screenshot 1"
    width="100%"
/>

<img
    src="./images/analytics.png"
    alt="Screenshot 2"
    width="100%"
/>

### Technologies Used

#### Frontend

<img src="https://img.shields.io/badge/-React-1A82A7?style=for-the-badge&logo=react&logoColor=1A82A7&labelColor=black"> <img src="https://img.shields.io/badge/-SCSS-CF649B?style=for-the-badge&logo=sass&logoColor=CF649B&labelColor=black">

#### Backend

<img src="https://img.shields.io/badge/-Flask-257277?style=for-the-badge&logo=flask&logoColor=257277&labelColor=black"> <img src="https://img.shields.io/badge/-OpenAI-1EA683?style=for-the-badge&logo=openai&logoColor=1EA683&labelColor=black">

#### Database

<img src="https://img.shields.io/badge/-Qdrant-DE2D53?style=for-the-badge&logoColor=DE2D53&labelColor=black&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0yNzcuOTc5IDc1LjkwOUwyNzcuOTk1IDc1Ljg5OThMMTQ5Ljk5NiAyTDIyLjAwMzIgNzUuODk3OUwyMiA3NS44OTk4TDIyLjAwMzIgNzUuOTA4NlYyMjMuNjk4TDE1MC4wMDEgMjk3LjU5OUwxNTAuMDAxIDI5Ny42MDNMMTkwLjk0NyAyNzMuOTc4TDE5MC45NDggMjczLjk3NkwxOTAuOTQ3IDI3My45NzVWMjIzLjY5OUwxNTAuMDAxIDI0Ny4zNDVMNjUuNTMwMyAxOTguNTgxVjEwMS4wMzlMMTUwLjAwMSA1Mi4yNzcxTDIzNC40NzIgMTAxLjAzOVYyOTcuNjAxTDIzNC40NjkgMjk3LjU5OUwyMzQuNDc1IDI5Ny42MTNMMjc4IDI3Mi40OTJWNzUuOTExMkwyNzcuOTc5IDc1LjkwOVoiIGZpbGw9IiNEQzI0NEMiLz4KPHBhdGggZD0iTTEwOS4wNTYgMTI2LjE3OVYxNzMuNDQ0TDE1MC4wMDEgMTk3LjA4OEwxOTAuOTQ3IDE3My40NDRWMTI2LjE3N0wxOTAuOTQxIDEyNi4xOEwxOTAuOTIgMTI2LjE2TDE1MC4wMDEgMTAyLjUzMUwxMDkuMDYgMTI2LjE3MkwxMDkuMDU3IDEyNi4xOEwxMDkuMDU2IDEyNi4xNzlaIiBmaWxsPSIjREMyNDRDIi8+Cjwvc3ZnPgo=">

### Hosting Locally

> [!IMPORTANT]
> Ensure sure both `source/client/example.env` and `source/server/example.env` are renamed to `.env` and are properly configured before hosting locally.

#### Starting The Client

```bash
cd source/client # If not already in the client directory.
npm i -y         # Install dependencies.
npm start        # Start the client.
```

#### Starting The Server

```bash
cd source/server                # If not already in the server directory.
pip install -r requirements.txt # Install dependencies.
python3 app.py                  # Start the server.
```

### Future Plans

- Optimize loading speeds on the client by using memoization.
- Add a skeleton loading animation while the content is being fetched.
