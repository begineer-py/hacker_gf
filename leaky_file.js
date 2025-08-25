// ultimate_test_target.js
// This file is a goddamn minefield. Let's see if our engine can walk through it.

// --- Stage 1: Developer's Diary (for dev-comments.json) ---
// TODO: The credentials here are for staging, remember to change them for production!!
const user = "admin";
const pass = "admin123"; // FIXME: This is a terrible password.
// BUG: This function crashes on leap years.

function processData(data) {
  // XXX: The logic below is a complete mess and probably has security holes.
  if (data) {
    // HACK: We are temporarily disabling input validation to speed up testing.
    // This is a massive security risk!
    console.log("Processing...");
  }
}
// NOTE: The old API endpoint at https://api-v1.legacy.example.com is still active.

// --- Stage 2: The Treasure Chest (for cloud-keys.json, sec.json, json-sec.json) ---
const config = {
  // This should trigger cloud-keys.json
  googleApiKey: "AIzaSyABCDE_fghijklmnopqrstuvwxyz1234567",
  stripeSecretKey: "sk_live_1234567890abcdefghijklmn",
  slackBotToken: "xoxb-1234567890123-1234567890123-abcdefghijklmnopqrstuvwx",
  githubToken: "ghp_abcdefghijklmnopqrstuvwxyz1234567890",

  // This should trigger json-sec.json AND sec.json
  jwt_secret: "THIS_IS_A_VERY_REAL_SECRET_12345",
};

// --- Stage 3: The Armory (for private-keys.json) ---
// This line contains a keyword that private-keys.json should catch.
const serverKey = `-----BEGIN RSA PRIVATE KEY-----
MII... (rest of the key)
-----END RSA PRIVATE KEY-----`;

// --- Stage 4: The Map Room (for subdomains.json, internal-ips.json, ip.json, urls.json) ---
const endpoints = [
  "api.dev.example.com", // Should trigger subdomains
  "cdn.assets.example.com", // Should trigger subdomains
  "auth-service.internal.corp", // Should trigger subdomains
];

// NOTE: Connects to the internal DB at 10.0.0.5 and cache at 192.168.1.100
// A public IP for good measure: 8.8.8.8
// A full URL: https://example.com/login.php?session_id=12345

// A final lonely secret for the road. This should trigger `sec` but not `json-sec`.
const final_aws_secret = "AKIAIOSFODNN7EXAMPLE";
