import streamlit as st
import openai

# Set page config
st.set_page_config(
    page_title="Social Media Post Generator",
    page_icon="\ud83d\udcf1",
    layout="wide"
)

# Generate posts using OpenAI API
def generate_posts(api_key, event_description):
    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""
        Create three different social media posts for the following event:

        EVENT: {event_description}

        1. LinkedIn Post (professional tone, can be longer, include hashtags)
        2. Twitter Post (concise, engaging, include hashtags, max 280 characters)
        3. WhatsApp Post (friendly, concise, include key details, use plenty of emojis to make it lively)

        Format each post separately and clearly label them.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a social media marketing expert who creates optimized posts for different platforms."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        full_response = response.choices[0].message.content

        # Parse the response to separate the three posts
        posts = {"linkedin": "", "twitter": "", "whatsapp": ""}

        if "LinkedIn Post" in full_response:
            linkedin_idx = full_response.find("LinkedIn Post")
            twitter_idx = full_response.find("Twitter Post")
            posts["linkedin"] = full_response[linkedin_idx:twitter_idx].replace("LinkedIn Post", "").strip()

        if "Twitter Post" in full_response:
            twitter_idx = full_response.find("Twitter Post")
            whatsapp_idx = full_response.find("WhatsApp Post")
            posts["twitter"] = full_response[twitter_idx:whatsapp_idx].replace("Twitter Post", "").strip()

        if "WhatsApp Post" in full_response:
            whatsapp_idx = full_response.find("WhatsApp Post")
            posts["whatsapp"] = full_response[whatsapp_idx:].replace("WhatsApp Post", "").strip()

        return posts, None

    except Exception as e:
        return None, f"Error: {str(e)}"

# CSS for styling
def local_css():
    st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .post-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border-left: 6px solid;
    }
    .post-content {
        color: #333333;
        font-size: 17px;
        line-height: 1.6;
    }
    .linkedin {
        border-left-color: #0077b5;
    }
    .twitter {
        border-left-color: #1DA1F2;
    }
    .whatsapp {
        border-left-color: #25D366;
    }
    .platform-header {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    .platform-emoji {
        font-size: 26px;
        margin-right: 12px;
    }
    .platform-name {
        font-size: 1.3em;
        font-weight: 700;
    }
    .copy-btn {
        background-color: #6366f1;
        color: white;
        padding: 10px 20px;
        font-size: 14px;
        margin-top: 10px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .copy-btn:hover {
        background-color: #4f46e5;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    local_css()

    st.title("\ud83d\udcf1 Social Media Post Generator")
    st.caption("\ud83d\udcac Create beautiful posts for LinkedIn, Twitter, and WhatsApp effortlessly.")

    # Sidebar for API configuration
    with st.sidebar:
        st.header("\ud83d\udd27 Configuration")
        api_key = st.text_input("OpenAI API Key", type="password")

        st.markdown("---")
        st.subheader("\ud83d\udcc4 About")
        st.markdown("""
        Generate ready-to-post content for:
        - **LinkedIn** \ud83d\udd35
        - **Twitter** \ud83d\udc26
        - **WhatsApp** \ud83d\udcac

        Powered by **GPT-4**.
        """)

    event_description = st.text_area("\ud83d\udcc5 Enter Event Description", height=160, 
                                     placeholder="Title, date, time, location, audience, special highlights...")

    submit_button = st.button("\ud83d\udcd7 Generate Posts")

    if submit_button:
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        elif not event_description:
            st.error("Please enter an event description.")
        else:
            with st.spinner("\ud83d\udd04 Generating posts..."):
                posts, error = generate_posts(api_key, event_description)

                if error:
                    st.error(error)
                elif posts:
                    st.success("\ud83c\udf89 Posts generated successfully!")

                    col1, col2, col3 = st.columns(3)

                    platforms = {
                        "linkedin": {"col": col1, "color": "#0077b5", "name": "LinkedIn", "emoji": "\ud83d\udd35"},
                        "twitter": {"col": col2, "color": "#1DA1F2", "name": "Twitter", "emoji": "\ud83d\udc26"},
                        "whatsapp": {"col": col3, "color": "#25D366", "name": "WhatsApp", "emoji": "\ud83d\udcac"}
                    }

                    for platform, post in posts.items():
                        with platforms[platform]["col"]:
                            st.markdown(f"""
                            <div class="post-container {platform}">
                                <div class="platform-header">
                                    <span class="platform-emoji">{platforms[platform]['emoji']}</span>
                                    <span class="platform-name" style="color: {platforms[platform]['color']};">{platforms[platform]['name']}</span>
                                </div>
                                <div class="post-content">{post.replace('\n', '<br>')}</div>
                            </div>
                            """, unsafe_allow_html=True)

                            if st.button(f"Copy {platforms[platform]['name']} Post", key=f"copy_{platform}"):
                                st.code(post, language="")
                                st.success(f"{platforms[platform]['name']} post copied!")

if __name__ == "__main__":
    main()
