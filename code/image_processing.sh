# Directory containing the images
input_directory="./../data/2019_confocal_cavity"
output_directory="./../plots/2019_confocal_cavity"

# Second limit if increased will contain more faint black (inverted), which might include backgnd noise

# Single image processing
filename="01"

# Construct the output filename
output_filename="${filename}_adjusted.png"
# Adjust contrast and save the new image
magick "${input_directory}/${filename}.bmp" -negate -colorspace Gray -level 10%,50% "${output_directory}/${output_filename}"
echo "Processed: ${filename}.bmp -> ${output_filename}"


# Loop through all image files in the input directory
# for image in "$input_directory"/*.bmp; do
#   # Get the filename without the directory path
#   filename=$(basename "$image" .bmp)
  
#   # Construct the output filename
#   output_filename="${filename}_adjusted.png"
  
#   # Adjust the contrast and save the new image
#   magick "$image" -negate -colorspace Gray -level 55%,85% "$output_directory/$output_filename"
  
#   # Print a message indicating the image has been processed
#   echo "Processed: $filename -> $output_filename"
# done