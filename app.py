from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

qa_pairs = {
    # Greetings
    "hello": "Welcome to our company! How may I assist you today?",
    "hi": "Hello! I'm BingoAI, your virtual front desk assistant.",
    "hey": "Hi there! How can I help you?",
    "good morning": "Good morning! Welcome to our company. How may I assist you today?",
    "good afternoon": "Good afternoon! How may I assist you today?",
    "good evening": "Good evening! I'm here to help you.",
    "how are you": "I'm functioning perfectly. How can I assist you?",
    "who are you": "I am BingoAI, your virtual front desk assistant. I answer your queries and provide you insight about our company.",
    "what can you do": "I can provide information about our company, services and support.",
    "are you a robot": "Yes, I am an AI-powered virtual assistant designed to help you.",

    # Company Information
    "what is the name of your company": "Our company is called BingoAI.",
    "company name": "Our company is called BingoAI.",
    "when was your company established": "Our company was established in 2026, to be precise April 24, 2026.",
    "what does your company do": "We specialize in AI solutions, web development and digital services.",
    "what industry do you operate in": "We operate in the technology and artificial intelligence industry.",
    "who is the founder": "The founder of our company is Miss Thanuja Sri.",
    "where is your headquarters": "Our headquarters are located in Madurai, Tamil Nadu, India.",
    "what is your mission": "Our mission is to deliver innovative and intelligent digital solutions to everyone in need.",
    "what is your vision": "Our vision is to empower businesses through cutting-edge technology.",
    "what makes your company unique": "We combine creativity, innovation and AI-driven solutions.",
    "what type of company": "We specialize in AI solutions, web development and digital services.",

    # Services
    "what services do you offer": "We offer AI solutions, web development and automation services. We also train students with information technology knowledge.",
    "services": "We offer AI solutions, web development, and automation services. We also train students with information technology knowledge.",
    "do you provide web development": "Yes, we specialize in modern and responsive web development.",
    "do you develop mobile applications": "Yes, we develop high-performance mobile applications.",
    "do you offer ai solutions": "Yes, we provide customized AI-powered solutions.",
    "do you build chatbots": "Yes, we design intelligent chatbots for businesses and educational purposes.",
    "do you provide machine learning services": "Yes, we develop machine learning models and applications.",
    "do you offer cloud services": "Yes, we provide scalable cloud-based solutions.",
    "do you provide ui ux design": "Yes, we create intuitive and engaging user interfaces.",
    "do you offer automation services": "Yes, we streamline business processes using automation.",
    "can you customize software": "Absolutely! We develop tailor-made software solutions.",
    "total employees working in the company": "about 80 skillful and experienced developers and 10 experienced trainers are currently employed here.",
    "number of employees working in the company": "about 80 skillful and experienced developers and 10 experienced trainers are currently employed here.",
    "how many employees are working in the company": "there are about 80 skillful and experienced developers and 10 experienced trainers are currently employed here.",

    # Working Hours
    "what are your working hours": "Our office is open from 9 AM to 6 PM, Monday to Friday.",
    "business hours": "Our office is open from 9 AM to 6 PM, Monday to Friday.",
    "are you open on weekends": "Sorry! We are closed on weekends.",
    "when can i contact support": "You can contact support during our working hours.",
    "are you available 24/7": "Our AI assistant is available 24/7, but our office operates from 9 AM to 6 PM, Monday to Friday.",
    "do you operate internationally": "Yes, we serve clients globally.",

    # Location & Contact
    "where are you located": "We are located in Madurai, Tamil Nadu, India.",
    "location": "We are located in Madurai, Tamil Nadu, India.",
    "what is your office address": "Our address is Building Number 22, Church Street, Madurai, Tamil Nadu, India.",
    "how can i contact you": "You can contact us via phone or email.",
    "contact": "You can contact us via phone or email.",
    "phone number": "You can reach us at +91 78965 41230.",
    "what is your email address": "Our email is contact@bingoai.com.",
    "email": "Our email is contact@bingoai.com.",
    "do you have a website": "Yes, please visit our website at www.bingoai.com.",
    "can i visit your office": "Yes, visitors are welcome during office hours.",
    "do you offer online consultations": "Yes, we offer virtual consultations.",
    "how do i schedule a meeting": "Please contact us via email or phone to schedule a meeting.",
    "do you have social media pages": "Yes, you can follow us on our official social media platforms.",
    "how many branches do you have" : "as of now we only have one branch ",

    # Pricing & Projects
    "how much do your services cost": "Pricing depends on project requirements. Usually work starts from Rupees 8000.",
    "do you offer free consultations": "Yes, we provide an initial free consultation.",
    "do you offer customized pricing": "Yes, we tailor pricing to meet client needs.",
    "what payment methods do you accept": "We accept cash, bank transfers and digital payments.",
    "do you work with startups": "Yes, we collaborate with startups and enterprises.",
    "how long does a project take": "Project timelines depend on complexity.",
    "do you provide project support": "Yes, we offer ongoing support and maintenance.",
    "can i get a quotation": "Certainly! Please contact us for a detailed quotation.",
    "do you sign ndas": "Yes, we respect confidentiality and sign NDAs.",
    "do you provide maintenance services": "Yes, we offer post-deployment maintenance depending on the project.",

    # Careers & Internships
    "do you have job openings": "Please check our careers page for current opportunities.",
    "how can i apply for a job": "You can apply via our website or email your resume.",
    "do you offer internships": "Yes, we provide internship opportunities.",
    "do you hire freshers": "Yes, we welcome talented fresh graduates.",
    "what skills do you look for": "We look for skills in programming languages, AI and problem-solving.",

    # Policies & Support
    "do you protect customer data": "Yes, we prioritize data security and privacy.",
    "do you have a privacy policy": "Yes, our privacy policy is available on our website.",
    "do you provide technical support": "Yes, we offer dedicated technical support.",
    "how do i report an issue": "Please contact our support team.",
    "do you offer refunds": "Refunds are subject to our terms and conditions.",

    # Partnerships & Clients
    "do you collaborate with other companies": "Yes, we welcome partnerships.",
    "who are your clients": "We serve businesses across multiple industries.",
    "can we partner with your company": "Certainly! Please contact us for collaboration.",
    "do you handle enterprise projects": "Yes, we handle projects of all scales.",
    "do you work internationally": "Yes, we work with global clients all across the world.",

    # Portfolio & Achievements
    "can i see your portfolio": "Yes, our portfolio is available on our website. You can check it on bingoai.com.",
    "have you completed successful projects": "Yes, we have delivered numerous successful projects.",
    "do you have client testimonials": "Yes, testimonials are available on our website.",
    "have you received any awards": "Yes, we have been recognized for excellence in innovation.",
    "what technologies do you use": "We use modern technologies like Python, AI and cloud platforms.",

    # Training & Education
    "do you offer training programs": "Yes, we provide training in AI and web development.",
    "do you conduct workshops": "Yes, we conduct technical workshops and seminars.",
    "do you offer certification courses": "Yes, certification programs are available.",
    "are your courses beginner-friendly": "Yes, our courses cater to all skill levels.",
    "do you provide online learning": "Yes, we offer online training sessions.",

    # Miscellaneous
    "can you help me today": "Certainly! How may I assist you?",
    "thank you": "You're welcome! Have a great day.",
    "thanks": "My pleasure! Let me know if you need anything else.",
    "that is helpful": "I'm glad I could assist you.",
    "i need more information": "Please let me know your query in detail.",
    "can i speak to a human representative": "Certainly! I will connect you to our team.",
    "do you provide customer support": "Yes, our support team is always ready to assist you.",
    "are you available now": "Yes, I am available to assist you.",
    "can you repeat that": "Of course! Please let me know what you need again.",
    "could you help me with my query": "Certainly! Please provide more details.",

    # Closing Interactions
    "goodbye": "Thank you for visiting us. Have a wonderful day!",
    "bye": "Goodbye! We look forward to serving you again.",
    "see you later": "See you soon! Have a great day.",
    "talk to you later": "Looking forward to assisting you again.",
    "have a nice day": "Thank you! Wishing you a pleasant day.",
    "have a great day": "Thank you! Take care.",
    "thats all": "Happy to help! Let me know if you need anything else.",
    "i am done": "Thank you for your time. Goodbye!",
    "end conversation": "Thank you for contacting us. Have a great day!",
    "exit": "Thank you for visiting BingoAI. Goodbye!"
}

synonym_map = {
    "address": "what is your office address",
    "office address": "what is your office address",
    "company address": "what is your office address",
    "head office": "what is your office address",
    "location": "where are you located",
    "where is your office": "where are you located",
    "phone": "phone number",
    "mobile": "phone number",
    "contact number": "phone number",
    "mail": "email",
    "email id": "email",
    "website": "do you have a website",
    "site": "do you have a website",
    "cost": "how much do your services cost",
    "price": "how much do your services cost",
    "fees": "how much do your services cost",
    "timing": "what are your working hours",
    "hours": "what are your working hours",
    "open": "what are your working hours",
    "close": "what are your working hours",
    "internship": "do you offer internships",
    "jobs": "do you have job openings",
    "career": "do you have job openings",
    "support": "do you provide technical support",
    "help": "can you help me today",
    "services offered": "what services do you offer",
    "ceo" : "who is the founder",
    "established" : "when was your company established",
    "total employees" : "total employees working in the company",
    "number of employees": "number of employees working in the company",
    "how many employees": "how many employees are working in the company",
    "branch":"how many branches do you have",
    "branches":"how many branches do you have",
}

def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text

def get_ai_response(user_message):
    if not user_message:
        return "Please enter a message so I can assist you."

    message = normalize_text(user_message)

    if message in qa_pairs:
        return qa_pairs[message]

    for key, mapped_question in synonym_map.items():
        if key in message:
            return qa_pairs.get(mapped_question, "I'm here to help!")

    for question, answer in qa_pairs.items():
        if question in message or message in question:
            return answer

    message_words = set(message.split())
    for question, answer in qa_pairs.items():
        question_words = set(question.split())
        if message_words & question_words:
            return answer

    return (
        "I'm sorry, I couldn't find the information you're looking for. "
        "Please contact our support team for further assistance."
    )


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    response = get_ai_response(user_message)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)