from google import google, images
options = images.ImageOptions()
options.image_type = images.ImageType.CLIPART
options.larger_than = images.LargerThan.MP_4
options.color = "green"
results = google.search_images("banana", options)
