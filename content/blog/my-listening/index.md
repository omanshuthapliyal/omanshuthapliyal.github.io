---
title: "Music to my Peers"
date: 2026-10-02T09:00:00-07:00
draft: false
tags: ["music", "data"]
---

Terrible pun aside, I realized that I had recently completed 10 years of listening on Spotify and wanted to dig a little bit into my listening habits, especially how they have evolved over time.
Though admittedly, my listening habits have changed a lot and I no longer find as much time to explore new artists (at least as much as I would like to), I thought maybe I should get my hands on some of that sweet Spotify data for about a decade and maybe do some exploratory data analysis.
I realized that Spotify makes it a little difficult to get your hands on your own account lifetime data, but after a couple days of requesting, I received a small .zip file with data for ~41,000 tracks heard in about 10 years.

I quickly realized that I am quite the Spotify power user, with over 1600 listening days, of the ~3,500 days, amounting to a roughly 50% days of Spotify usage one way or another. 
In fact, during peak COVID in 2020, my average daily listening clocked in at about 100 minutes every day.
So this got me thinking about an "internal rewind" to see if I can reminisce any events across the past listening history, and I got Claude to cook up an EDA tool (that I later had it polished to generate reportable figures, which is what you see here) that [can be found here](https://github.com/omanshuthapliyal/your-spotify) to run locally on your own data!
I mostly wanted to see if my listening evolution had any patterns that can be observed, but I was pleasantly surprised to find various other key events!

{{< iframe-embed src="embeds/listening/artists-timeline.html" plot="artists-timeline" title="Artists over time" >}}

For instance, I can see a very clear increased usage during the COVID-19 lockdown periods, with a very sharp decline coinciding with my dissertation writing in its final phases.
I also see a few bands edging over others, right before I saw them live (King Gizzard & the Lizard Wizard, Tool and Vulfpeck)!

I can also see some patterns in a few songs that have been a constant during the last decade.
For instance, my go-to song on my weekly drive from UIUC to Purdue (In the Basement of the Alamo - TAUK)!

{{< iframe-embed src="embeds/listening/songs-timeline.html" plot="songs-timeline" title="Songs over time" >}}

On the other hand, it was unsurprising to see genres remain more or less the same, indicating that my listening habits themselves have changed, but preferences not so much.
But I do see a few genres growing on me in the last 2 years or so.
{{< iframe-embed src="embeds/listening/genres-timeline.html" plot="genres-timeline" title="Genres over time" >}}

But what I found most surprising was how predictable my listening patterns were! To me, I am trying to find new artists as much as I could, but it seems my listening habits followed the Pareto principle quite closely.
In fact, not only did a handful of artists make up almost all my listening history, they were tightly clustered among each other as well.
I tried to cluster them into 6 (seemingly quite coherent and tight) clusters, where artists that I tend to listen to together, appear together. 
  
{{< iframe-embed src="embeds/listening/map.html" plot="map" heading="Artists that are played together" description="" >}}

This was supposed to be an interesting map for me to hover around and find weird links (Chase & Status and Nirvana heard together?!) for myself, but in case it is inviting, [you can try it yourself](https://github.com/omanshuthapliyal/your-spotify).
And if you find an artist or track you like in here, or have something to recommend, drop me a message :)