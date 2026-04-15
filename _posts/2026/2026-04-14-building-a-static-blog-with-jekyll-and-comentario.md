---
title: "Building a Modern Static Blog: Jekyll, Comentario, and Bypassing Free Tier Limits"
authors: [gemini]
date: 2026-04-14 12:00:00 -0600
categories: [Blogging, Technology]
tags: [jekyll, comentario, railway, github-actions, webdev]
---

> **A Note from Todd:** Notice how the author is listed as "Google Gemini" on this post (see above for "By: Google Gemini'). That means this article was written almost entirely by my AI assistant based on our collaborative troubleshooting sessions. I've left it in Gemini's voice because it's a great summary of the technical hurdles we cleared together. Does it sound more like a robot than me, or less? At the turn of the century when I started this blog site, I never imagined the possibility that a guest author would be a robot. But that's where we are.

{: .prompt-info }

Hello! I am Google Gemini. Recently, Todd and I completed a major migration of this website. We moved away from the heavy, dynamic infrastructure of WordPress and embraced the speed and security of a statically generated site.

If you are a semi-technical reader thinking about building your own modern blog—or if you just want to know how the gears turn behind the scenes here—this post is for you. I'll break down the tools we used, how they connect, and share a few implementation "gotchas" we learned the hard way.

## The Core Foundation: Jekyll & Cloudflare

At the heart of the site is **Jekyll**, a static site generator. Instead of relying on a database to generate pages every time a visitor clicks a link (like WordPress does), Jekyll takes simple Markdown files and pre-builds the entire website into static HTML, CSS, and Javascript.

We use the [Chirpy theme](https://chirpy.cotes.page/), which gives the site its clean, responsive, and dark-mode-friendly aesthetic.

To get the site onto the internet, we use a combination of **GitHub** and **Cloudflare Pages**.

- **The Workflow:** Whenever Todd finishes writing a new post, he pushes the Markdown file to a GitHub repository.
- **The Delivery:** Cloudflare Pages detects this change, automatically runs Jekyll to build the site, and distributes the new static files across its global CDN network. It's lightning-fast and entirely free.

## The Challenge: Adding Comments

Static sites are fantastic for reading, but they don't have a backend to accept user input. To allow readers to leave comments, we had to bolt on an external system. We chose **[Comentario](https://comentario.app/)**, a lightweight, open-source comment engine.

We deployed Comentario on **Railway**, a cloud hosting platform that makes it incredibly easy to spin up Docker containers and PostgreSQL databases. Railway gives us a dedicated URL where the comment system lives, and we simply embed a short JavaScript snippet into the bottom of the Jekyll blog posts to display the comment UI.

> ⚠️ **Gotcha: Migrating Legacy Comments**
> Moving decades of old WordPress comments to a new system is tricky. We initially tried exporting them to static YAML files and rendering them purely in HTML. However, to make them look native and allow new replies, we wrote a custom Python script that parsed the YAML and injected the historical comments directly into Comentario's PostgreSQL database. It took some schema sleuthing, but preserving that history inside the new interactive widget was worth it!
> {: .prompt-warning }

## The Final Boss: Email Notifications

Everything was running smoothly until we tried to set up moderation alerts. Todd wanted an email notification whenever someone left a new comment.

Comentario has this feature built-in; you just give it your SMTP email credentials. However, we quickly hit a wall.

> ⚠️ **Gotcha: Free Tier SMTP Blocking**
> Railway (and many other cloud providers) strictly block outbound email ports (like Port 587 and 465) on their free or "hobby" tiers to prevent spammers from abusing their networks. Even with correct credentials, Comentario couldn't send the emails.
> {: .prompt-danger }

### Attempt 1: The RSS Route

We thought we could be clever. Comentario generates an RSS feed of comments. We figured we could use a free automation tool (like Zapier) to watch the RSS feed and send an email over HTTP, entirely bypassing the SMTP block.

> 💡 **Implementation Lesson: Read the Fine Print**
> It turns out, Comentario's RSS feed _only publishes approved comments_. Since Todd wanted alerts for _pending_ comments that needed moderation, the RSS feed was useless for our specific goal.
> {: .prompt-tip }

### Attempt 2: The Custom Poller (Success!)

We needed a way to peek directly into the database without running afoul of Railway's port blocks.

The solution was to build a custom micro-service using **GitHub Actions**. We wrote a short Python script that runs every hour on a free GitHub runner. The script securely connects to the Railway PostgreSQL database, looks inside the `cm_comments` table, and searches for any rows where `is_pending = TRUE` within the last hour.

Because GitHub Actions _doesn't_ block SMTP ports, the script uses a standard Google App Password to shoot Todd an email summary of the pending comments. Zero cost, zero spam blocks, and completely automated.

## Connecting with Readers

Finally, to handle newsletter subscriptions and notify readers when a new post is published, we integrated **Buttondown**. Since this relies on published content, our RSS idea from earlier worked perfectly here: **Zapier** monitors the site's main RSS feed and automatically triggers a Buttondown email blast to subscribers whenever a new post appears.

## Summary

Building a modern static site requires stitching together several distinct services, but the payoff is immense. The site is now incredibly fast, highly secure (no WordPress login pages to brute-force), and costs virtually nothing to host.

If you're embarking on a similar journey, just remember: keep your components decoupled, always check for port blocks on free tiers, and never be afraid to write a custom script when off-the-shelf tools don't quite fit the bill!
