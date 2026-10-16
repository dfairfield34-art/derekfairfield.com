# Stripe Integration Plan: Two Valley Intelligence

> **Status: UNOFFICIAL DRAFT.** Written from general Stripe knowledge, NOT from Stripe's `stripe_implementation_planner` (blocked in the build environment). Re-check each step against https://docs.stripe.com before going live. Re-run the official planner from your own machine when possible.

**Business:** twovalleyintelligence.com (Two Valley Intelligence, billed through Fairfield Kr8tive LLC)
**Products requested:** Payments, Billing, Invoicing, Tax, Connect

## The one thing that moves money

Get one paid offer live with a Stripe link. Everything else comes after the first dollar lands.

## Ground rules (read first)

1. **Test mode first.** Use `sk_test_` / `pk_test_` keys until a full test purchase works. Live mode is a separate switch.
2. **Secret keys never go in the repo, in chat, or in front-end code.** They live in environment variables on the host. Only the publishable key (`pk_`) is safe in a browser.
3. **Derek approves** before: switching to live mode, any DNS change, anything that spends money, anything touching production.
4. **Use a restricted key** (Stripe Dashboard > Developers > API keys) for server code, with only the permissions it needs.
5. **Legal entity:** the Stripe account belongs to Fairfield Kr8tive LLC (EIN, business bank account). Public-facing name on receipts: Two Valley Intelligence.

## What to use for each product (and when)

| Product | Use it for | Phase |
|---|---|---|
| **Payments** (Checkout / Payment Links) | One-off sales: audits, website builds, setup fees | 1 (now) |
| **Invoicing** | Custom-quote client work (net-15/30, send by email) | 1 (now) |
| **Billing** (Subscriptions + Customer Portal) | Monthly retainers: agents, automations, dashboards, maintenance | 2 |
| **Tax** (Stripe Tax) | Auto-calculate sales tax/VAT on the above | 2 (turn on before volume) |
| **Connect** | Only if you pay out to other parties (affiliates, contractors, a marketplace) | 4 (probably not needed yet) |

Plain answer on Connect: if clients pay you and you keep the money, you do **not** need Connect. Skip it until you split payments with someone else.

## Phase 0: Account setup (no code, ~1 hour)

- [ ] Create/verify the Stripe account for Fairfield Kr8tive LLC (business details, EIN, bank account).
- [ ] Set public business name, support email, statement descriptor (e.g. `TWOVALLEY INTEL`).
- [ ] Add branding (logo, colors) for Checkout, invoices, and receipts.
- [ ] Turn on 2-factor auth for every Stripe login.
- [ ] Stay in **test mode** for everything below.

## Phase 1: First paid offer (Payments + Invoicing)

Fastest path, no backend: **Payment Links** and **Invoices** from the Dashboard.

- [ ] Create a Product + Price for each offer (e.g. "AI Agent Audit", "Website Build: Deposit").
- [ ] Create a Payment Link per offer. Test with card `4242 4242 4242 4242`, any future date, any CVC.
- [ ] Put a "Pay / Book" button on twovalleyintelligence.com pointing at the link (a plain `<a href>`, no secrets involved).
- [ ] For custom quotes: create a Customer, then an Invoice (send by email, due in 15 or 30 days). Enable card + ACH bank transfer to cut fees on large invoices.
- [ ] Turn on email receipts.

**Exit test:** a full test-mode purchase completes and the receipt arrives.

## Phase 2: Recurring revenue and tax (Billing + Tax)

- [ ] Create recurring Prices (monthly retainer tiers; optional annual with a discount).
- [ ] Enable the **Customer Portal** so clients update cards and cancel without emailing you.
- [ ] Enable **Stripe Tax**: set your business address, add your registrations, and use `automatic_tax: { enabled: true }` on Checkout/Invoices/Subscriptions. Mark each Product with the correct tax code (software/SaaS vs services). Confirm with your CPA which states you must collect in before you register anywhere.
- [ ] Set up dunning (Billing > Settings): smart retries and failed-payment emails.

## Phase 3: Small backend (when Payment Links stop being enough)

Needed when you want accounts, gated dashboards, or automated onboarding after payment.

Recommended: serverless functions on the host you already use (Vercel or Cloudflare Workers) rather than a server to babysit.

Endpoints:
1. `POST /api/create-checkout-session`: creates a Checkout Session (`mode: payment` or `subscription`), returns the URL. Price IDs come from server config, **never from the browser**.
2. `POST /api/stripe-webhook`: the source of truth for "did they pay".
3. `POST /api/create-portal-session`: sends a customer to the Customer Portal.

Webhook must-haves:
- [ ] Verify the signature with the raw request body and the `whsec_` signing secret.
- [ ] Handle at minimum: `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`.
- [ ] **Idempotent:** store processed `event.id` values so a retried event does nothing twice.
- [ ] Return 2xx quickly; do slow work after responding.
- [ ] Grant access from webhooks, never from the success-page redirect.

Environment variables (host dashboard, never committed):
`STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PUBLISHABLE_KEY`, `SITE_URL`

Local testing: Stripe CLI (`stripe listen --forward-to localhost:3000/api/stripe-webhook`).

## Phase 4: Connect (only if needed)

Decide first: are you paying someone else out of customer payments?
- No → skip.
- Yes, affiliates/contractors → **Express** accounts with transfers.
- Yes, a marketplace → talk to Stripe sales; compliance load is much higher.

## Go-live checklist (Derek signs off on each)

- [ ] Full test purchase, refund, failed card (`4000 0000 0000 0002`), and subscription cancel all behave correctly.
- [ ] Webhook endpoint registered in **live** mode with its own live `whsec_`.
- [ ] Live keys added to the host environment only. Test keys removed from live.
- [ ] Refund/terms/privacy pages linked from the site (Stripe and card networks expect them).
- [ ] Footer on the site: `© 2026 Two Valley Intelligence · A Fairfield Kr8tive LLC brand`.
- [ ] One real $1-style live charge, then refund it.
- [ ] Tax registrations confirmed with CPA.

## Cost note (verify current pricing at stripe.com/pricing)

Standard card processing is roughly 2.9% + 30¢ per charge in the US. Billing, Tax, and Invoicing carry additional per-use fees, and Connect adds its own. Confirm current rates before choosing a pricing model.

## Open questions for Derek

1. What is the first offer, and at what price?
2. Retainer (monthly) or one-off projects first?
3. Which states/countries are clients in? (drives Tax)
4. Which host serves twovalleyintelligence.com? (drives Phase 3 setup)

## Next action

Phase 0 and Phase 1 need no code. Start with the Stripe Dashboard in test mode and create one Payment Link.
