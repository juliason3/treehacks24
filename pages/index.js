import { useState } from 'react';
import { Flex, Box } from 'reflexbox';

export default function Home() {
  const [formData, setFormData] = useState({
    skinType: '',
    skinTone: '',
    skinConditions: [],
    image: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleConditionChange = (e) => {
    const { value, checked } = e.target;
    let newConditions = formData.skinConditions;
    if (checked && !newConditions.includes(value)) {
      newConditions.push(value);
    } else {
      newConditions = newConditions.filter((condition) => condition !== value);
    }
    setFormData({ ...formData, skinConditions: newConditions });
  };

  const handleImageChange = (e) => {
    setFormData({ ...formData, image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append('skinType', formData.skinType);
    data.append('skinTone', formData.skinTone);
    formData.skinConditions.forEach((condition) => {
      data.append('skinConditions', condition);
    });
    data.append('image', formData.image);

    // Replace '/api/submit-form' with your actual Flask endpoint
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: data,
    });

    if (response.ok) {
      // Handle the response from the server
      console.log('Form submitted successfully!');
    } else {
      console.error('Failed to submit form');
    }
  };

  const formStyle = {
    border: '2px solid #FF8A48',
    padding: '20px',
    borderRadius: '10px',
    maxWidth: '600px',
    margin: 'auto',
    backgroundColor: 'white',
  };

  const buttonStyle = {
    backgroundColor: '#FF8A48',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '20px',
    cursor: 'pointer',
    marginTop: '20px',
    width: '100%',
  };

  // Single return statement for the component
  return (
    <Flex flexDirection="column" alignItems="center" justifyContent="center" height="100vh">
      <Box as="form" onSubmit={handleSubmit} sx={formStyle}>
        <h1 style={{ color: '#FF8A48', textAlign: 'center' }}>Sunscreenify</h1>

        {/* Skin Type Selection */}
        <Box mb={3}>
          <label htmlFor="skinType" style={{ color: '#FF8A48' }}>What is your skin type?</label>
          <select id="skinType" name="skinType" onChange={handleInputChange} className="form-control" defaultValue="">
            <option value="" disabled>Select your skin type</option>
            <option value="oily">Oily</option>
            <option value="dry">Dry</option>
            <option value="combination">Combination</option>
            <option value="sensitive">Sensitive</option>
            <option value="normal">Normal</option>
          </select>
        </Box>

        {/* Skin Tone Selection */}
        <Box mb={3}>
          <label htmlFor="skinTone" style={{ color: '#FF8A48' }}>What is your skin tone?</label>
          <select id="skinTone" name="skinTone" onChange={handleInputChange} className="form-control" defaultValue="">
            <option value="" disabled>Select your skin tone</option>
            <option value="pale">Pale</option>
            <option value="light_tan">Light Tan</option>
            <option value="golden_olive">Golden or Olive</option>
            <option value="dark_brown">Dark Brown</option>
            <option value="deep_brown">Deep Brown</option>
          </select>
        </Box>

        {/* Skin Conditions Selection */}
        <fieldset>
          <legend style={{ color: '#FF8A48' }}>Do you have any skin conditions? (select all)</legend>
          <Box mb={3}>
            <label><input type="checkbox" value="acne" onChange={handleConditionChange} /> Acne</label>
            <label><input type="checkbox" value="rosacea" onChange={handleConditionChange} /> Rosacea</label>
            <label><input type="checkbox" value="dermatitis" onChange={handleConditionChange} /> Dermatitis</label>
            {/* ... more checkboxes for other conditions ... */}
          </Box>
        </fieldset>

        {/* Image Upload */}
        <Box mb={3} style={{ textAlign: 'center' }}>
          <label htmlFor="imageUpload" style={{ color: '#FF8A48', cursor: 'pointer' }}>
            <strong>Upload sunscreen label</strong>
            <input type="file" id="imageUpload" name="image" onChange={handleImageChange} style={{ display: 'none' }} />
          </label>
        </Box>

        {/* Submit Button */}
        <Box mb={3}>
          <button type="submit" style={buttonStyle}>Submit</button>
        </Box>
      </Box>
    </Flex>
  );

}


/*

export default function Home() {
  const [file, setFile] = useState(null);
  const router = useRouter();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a file.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      router.push({
        pathname: '/summary',
        query: { text: data.text }, // Pass the extracted text as a query parameter
      });
    } else {
      alert('Failed to upload and extract text.');
    }
  };

  return (
    <Flex flexDirection="column" alignItems="center" justifyContent="center" height="100vh">
      <Box as="form" onSubmit={handleSubmit} width={[1, 1/2, 1/4]} px={2}>
        <h1>Upload Sunscreen Image</h1>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </Box>
    </Flex>
  );
}
*/