import React, { useState } from 'react';
import axios from 'axios';
import "./App.css"

function App() {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://localhost:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      console.log('File uploaded successfully:', response.data);
      // Pass the file path to the extractText function
      setExtractedText(response.data.content);
    })
    .catch(error => {
      console.error('Error uploading file:', error);
    });
  };

  const extractText = (filePath) => {
    console.log('Extracting text from file:', filePath); // Debugging statement
    axios.get(`http://localhost:5000/extract?file=${encodeURIComponent(filePath)}`) // Encode file path
    .then(response => {
      console.log('Text extracted successfully:', response.data);
      // Set extracted text if available in response
      if (response.data && response.data.message) {
        setExtractedText(response.data.message);
      } else {
        setExtractedText(''); // Clear extracted text if no message is available
      }
    })
    .catch(error => {
      console.error('Error extracting text:', error);
      setExtractedText(''); // Clear extracted text on error
    });
  };

  const copyText = () => {
    navigator.clipboard.writeText(extractedText)
      .then(() => {
        alert('Text copied to clipboard');
      })
      .catch(err => {
        console.error('Error copying text: ', err);
      });
  };

  return (
    <div className="App">
      <div className='titleBox'>
        <h1>Extract PDF</h1>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} className="btn-upload">Upload PDF</button>
      </div>
      
      
      <div className="ExtractedText">
        <h2>Extracted Text:</h2>
        <div className="text-box">
          <p>{extractedText}</p>
        </div>
        <button onClick={copyText} className="copy-text">Copy text</button>
      </div>

    </div>
  );
}

export default App;
