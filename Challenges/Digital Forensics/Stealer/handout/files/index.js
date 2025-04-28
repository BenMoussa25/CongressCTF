const express = require('express');
const cors = require('cors'); // Import cors
const bcrypt = require('bcryptjs');
const { validateEmail, hashPassword } = require('auth-help3r');
const { z } = require('zod');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;


app.use(cors({
    origin: '*'
}));

app.use(express.json());

// Simple in-memory "database" to store users
let users = [];

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

// Endpoint for user registration
app.post('/register', async (req, res) => {
  try {
    const parsedData = userSchema.parse(req.body);  // Validate input
    const { email, password } = parsedData;

    if (!validateEmail(email)) {
      return res.status(400).json({ error: 'Invalid email format.' });
    }

    // Hash password with email
    const hashedPassword = hashPassword(password,email)

    users.push({ email, password: hashedPassword });

    res.status(201).json({ message: 'User registered successfully.' });
  } catch (error) {
    res.status(400).json({ error: error.errors ? error.errors[0].message : error.message });
  }
});

// Endpoint for user login
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const user = users.find(u => u.email === email);
  if (!user) return res.status(401).json({ error: 'Invalid credentials.' });

  // Compare passwords using bcrypt
  const isPasswordValid = await bcrypt.compare(password, user.password);
  if (!isPasswordValid) return res.status(401).json({ error: 'Invalid credentials.' });

  res.status(200).json({ message: 'Login successful.' });
});

// Route for checking email validation (using auth-help3r)
app.get('/validate-email', (req, res) => {
  const { email } = req.query;
  if (!email) {
    return res.status(400).json({ error: 'Email parameter is required.' });
  }

  const isValid = validateEmail(email);
  res.status(200).json({ email, isValid });
});

// Serve the app
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
