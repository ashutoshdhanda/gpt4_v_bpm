css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
    <style>
        .response-container {
            display: block;
            max-width: 100%;
            overflow-x: auto;
        }
        .response-table {
            width: 100%;
            border-collapse: collapse;
        }
        .response-table td, .response-table th {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            white-space: nowrap;
        }
    </style>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

scrollable_box_css = """
<style>
.scrollable-box {
    height: 400px;  # Adjust the height as needed
    overflow-y: scroll;
    background-color: rgba(255, 255, 255, 0.5);  # Translucent background (you can adjust the opacity)
    padding: 10px;
    border-radius: 5px;
}
</style>
"""

# Define CSS to handle overflow
response_css = """
    <style>
        .response-container {
            display: block;
            max-width: 100%;
            overflow-x: auto;
        }
        .response-table {
            width: 100%;
            border-collapse: collapse;
        }
        .response-table td, .response-table th {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            white-space: nowrap;
        }
    </style>
"""
