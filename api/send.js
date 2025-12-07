// Vercel serverless function to forward enquiries to SendGrid (email) and Twilio (WhatsApp)
// Expects env vars: SENDGRID_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, ADMIN_EMAIL, ADMIN_WHATSAPP_TO

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    const { name, email, phone, message } = req.body || {};
    if (!name || !email || !message) {
      res.status(400).json({ error: 'Missing required fields' });
      return;
    }

    const sendgridKey = process.env.SENDGRID_API_KEY;
    const twilioSid = process.env.TWILIO_ACCOUNT_SID;
    const twilioAuth = process.env.TWILIO_AUTH_TOKEN;
    const twilioFrom = process.env.TWILIO_WHATSAPP_FROM; // e.g. 'whatsapp:+1415...'
    const adminWhats = process.env.ADMIN_WHATSAPP_TO; // e.g. 'whatsapp:+9190...'
    const adminEmail = process.env.ADMIN_EMAIL;

    // Compose email body
    const subject = `VoiceFlow Enquiry from ${name}`;
    const text = `Name: ${name}\nEmail: ${email}\nPhone: ${phone || 'N/A'}\n\nMessage:\n${message}`;

    // Send email via SendGrid REST API
    if (sendgridKey && adminEmail) {
      await fetch('https://api.sendgrid.com/v3/mail/send', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${sendgridKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          personalizations: [{ to: [{ email: adminEmail }] }],
          from: { email: email },
          subject: subject,
          content: [{ type: 'text/plain', value: text }]
        })
      });
    }

    // Send WhatsApp notification via Twilio REST API (if configured)
    if (twilioSid && twilioAuth && twilioFrom && adminWhats) {
      const form = new URLSearchParams();
      form.append('From', twilioFrom);
      form.append('To', adminWhats);
      form.append('Body', `${subject}: ${message.substring(0,300)} -- From: ${name} (${email})`);

      await fetch(`https://api.twilio.com/2010-04-01/Accounts/${twilioSid}/Messages.json`, {
        method: 'POST',
        headers: {
          Authorization: 'Basic ' + Buffer.from(`${twilioSid}:${twilioAuth}`).toString('base64'),
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: form.toString()
      });
    }

    res.status(200).json({ ok: true });
  } catch (err) {
    console.error('send handler error', err);
    res.status(500).json({ error: 'Internal server error' });
  }
}
