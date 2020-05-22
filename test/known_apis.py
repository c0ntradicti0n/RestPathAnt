apis =\
    {
        "api.cloudinay.com/{username}/{path}/v1_1/": (
            ["upload", "eager_transform"],
            {
            "username": "rastefan",
            "path": "sickfits"}
        ),

        "https://api.openstreetmap.org/api/0.6/": (
            ["map?bbox="],  # {left},{bottom},{right},{top}]
            ()
        ),

        "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&": (
            ["action=query&list=geosearch&"], # sgsradius=10000&gscoord=37.786971%7C-122.399677"
            ()
        )
    }
