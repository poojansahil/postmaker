import streamlit as st
import openai

# Set page config
st.set_page_config(
    page_title="Social Media Post Generator",
    page_icon="📱",
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
        3. WhatsApp Post (friendly, concise, include key details)
        
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
    .post-container {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid;
        color: #000000;  /* Explicitly set text color to black */
    }
    .post-content {
        color: #000000;  /* Ensure post content is black */
        font-size: 16px;
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
        margin-bottom: 10px;
    }
    .platform-emoji {
        font-size: 24px;
        margin-right: 10px;
    }
    .platform-name {
        font-size: 1.2em;
        font-weight: bold;
    }
    .copy-btn {
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    local_css()
    
    # Header
    st.title("📱 Social Media Post Generator")
    st.markdown("Generate professional posts for LinkedIn, Twitter, and WhatsApp from a single event description.")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("OpenAI API Key", type="password")
        
        # Information about the app
        st.markdown("---")
        st.subheader("About")
        st.markdown("""
        This app uses OpenAI's GPT-4 to generate optimized posts for different platforms:
        
        - **LinkedIn** 🔵: Professional, detailed
        - **Twitter** 🐦: Concise, engaging (280 chars)
        - **WhatsApp** 💬: Friendly, informative
        
        Enter your event details to generate posts!
        """)
    
    # Main content
    event_description = st.text_area("Enter Event Description", height=150, 
                                     placeholder="Describe your event with details like title, date, time, location, purpose, target audience, and any special features.")
    
    # Validate inputs before processing
    submit_button = st.button("Generate Posts")
    
    if submit_button:
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        elif not event_description:
            st.error("Please enter an event description.")
        else:
            with st.spinner("Generating posts..."):
                posts, error = generate_posts(api_key, event_description)
                
                if error:
                    st.error(error)
                elif posts:
                    st.success("Posts generated successfully!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    platforms = {
                        "linkedin": {"col": col1, "color": "#0077b5", "name": "LinkedIn", "emoji": "🔵"},
                        "twitter": {"col": col2, "color": "#1DA1F2", "name": "Twitter", "emoji": "🐦"},
                        "whatsapp": {"col": col3, "color": "#25D366", "name": "WhatsApp", "emoji": "💬"}
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
                            
                            # Copy button functionality
                            if st.button(f"Copy {platforms[platform]['name']} Post", key=f"copy_{platform}"):
                                st.code(post, language="")
                                st.success(f"{platforms[platform]['name']} post copied!")

if __name__ == "__main__":
    main()