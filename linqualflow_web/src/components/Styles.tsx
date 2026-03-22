import React from "react";

export const actionButtonStyle: React.CSSProperties = {
    padding: '15px 30px',
    fontSize: '16px',
    borderRadius: '10px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
};

export const backButtonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    color: '#666',
    marginBottom: '20px',
    padding: 0
};

export const buttonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',  // ТЕКСТ ПО ЦЕНТРУ (по горизонтали)
    gap: '10px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    fontWeight: 500,
    color: '#333'
};

export const menuButtonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    fontWeight: 500,
    color: '#333'
};

export const inputStyle: React.CSSProperties = {
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    fontSize: '16px',
    width: '100%',
    boxSizing: 'border-box'
};

export const logoutButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    color: '#d32f2f',
    borderColor: '#ffcdd2'
};

export const styles: Record<string, React.CSSProperties> = {

    container:{
        maxWidth:600,
        margin:"0 auto",
        padding:20,
        textAlign:"center"
    },

    question:{
        fontSize:24,
        marginBottom:30
    },

    optionsContainer:{
        display:"flex",
        flexDirection:"column",
        gap:12
    },

    optionButton:{
        padding:"12px 20px",
        fontSize:16,
        borderRadius:8,
        border:"1px solid #ccc",
        cursor:"pointer"
    },

    flashcardContainer:{
        marginTop:20
    },

    scrambleContainer:{
        display:"flex",
        flexDirection:"column",
        gap:12,
        alignItems:"center"
    },

    input:{
        padding:10,
        fontSize:16,
        width:200
    },
    correctButton: {
        padding: '10px 20px',
        backgroundColor: '#28a745',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontWeight: 'bold' as const
    },
    wrongButton: {
        padding: '10px 20px',
        backgroundColor: '#dc3545',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontWeight: 'bold' as const
    },
    primaryButton:{
        padding:"12px 20px",
        borderRadius:8,
        border:"none",
        background:"#007bff",
        color:"#fff",
        cursor:"pointer"
    },
    backspaceButton: {
        padding: '10px 15px',
        fontSize: '1.2rem',
        borderRadius: '8px',
        border: '1px solid #ccc',
        backgroundColor: '#f8f9fa',
        cursor: 'pointer',
        color: '#333',
        display: 'flex',
        alignItems: 'center'
    },
    secondaryButton: {
        padding: '10px 20px',
        borderRadius: '8px',
        border: '1px solid #ccc',
        backgroundColor: '#fff',
        cursor: 'pointer'
    },

}


export const formStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
};

export const submitButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    justifyContent: 'center',
    padding: '14px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    marginTop: '10px'
};

export const gridStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
    gap: '20px',
};

export const cardStyle: React.CSSProperties = {
    padding: '24px',
    backgroundColor: '#fff',
    borderRadius: '16px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
    textAlign: 'center',
    border: '1px solid #eee',
};

export const iconWrapperStyle = (bgColor: string): React.CSSProperties => ({
    width: '50px',
    height: '50px',
    borderRadius: '12px',
    backgroundColor: bgColor,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '0 auto 15px auto',
});

export const valueStyle: React.CSSProperties = {
    fontSize: '2rem',
    fontWeight: 'bold',
    margin: '10px 0 0 0',
    color: '#333',
};

export const centerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '80vh',
};


/* Стили
export const buttonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    fontWeight: 500,
    color: '#333'
};

export const menuButtonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    fontWeight: 500,
    color: '#333'
};


export const inputStyle: React.CSSProperties = {
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    fontSize: '16px',
    width: '100%',
    boxSizing: 'border-box'
};

export const formStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
};

export const submitButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    justifyContent: 'center',
    padding: '14px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    marginTop: '10px'
};

export const backButtonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    color: '#666',
    marginBottom: '20px',
    padding: 0
};
*/