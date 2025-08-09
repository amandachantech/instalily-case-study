// frontend/src/api/api.js
export const getAIMessage = async (userQuery) => {
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userQuery })
      });
  
      const data = await response.json();
  
      return {
        role: "assistant",
        content: data.response
      };
  
    } catch (error) {
      console.error("API error:", error);
      return {
        role: "assistant",
        content: "Server error. Please try again later."
      };
    }
  };
  