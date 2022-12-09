const express = require('express')
const app = express()
const port = 6000
const { OAuth2Client } = require('google-auth-library')
const client = new OAuth2Client(
  {
    clientId: process.env.CLIENTID,
    clientSecret: process.env.CLIENTSECRET,
    redirectUri: 'http://revuppaal.dk'
  }
)

app.use(express.json())
app.post('/google-verifier', (req, res) => {
  
  verifyCode(req.body.code).then((tokens) => {
    res.send(tokens)
  }).catch((error) => {
    console.log(error)
    res.send("something went wrong")
  })  
})



app.post('/google-verifier/token-verifier', (req, res) => {
  
  verifyToken(req.body.token).then((userInfo) => {
    res.send(userInfo)
  }).catch((error) => {
    console.log(error)
    res.send("something went wrong")
  })  
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})


// Call this function to validate OAuth2 authorization code sent from client-side
async function verifyCode(code) {
  console.log("VerifyCode entered, code: " + code)
  let { tokens } = await client.getToken(code)
  console.log("Printing tokens: " + tokens)
  console.log("Hello, I am a refresh token", tokens.refresh_token)

  return tokens
}

async function verifyToken(tokens) {
  
  client.setCredentials({ access_token: tokens.access_token })
  const userinfo = await client.request({
    url: 'https://www.googleapis.com/oauth2/v3/userinfo'
  })

  console.log(userinfo.data)

  return { email: userinfo.data.email }
}