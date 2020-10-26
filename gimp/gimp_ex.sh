
# Desc: Create growing explosion on transparent background





radius=10; ttt=1; for i in {1..30}; do gimp -i /home/joepers/Videos/DS3/kdenlive/highlights/ts.png -b "(plug-in-nova 1 1 2 500 500 \`(255 127 0) $radius 100 5)" -b "(file-png-save-defaults 1 1 2 \"$ttt.png\" \"rrr\")" -b '(gimp-quit 0)'; radius=$((radius*2)); ((ttt++)); done





-naidfs






# floor -
gimp -i ~/Videos/DS3/kdenlive/highlights/pp.png -b '(gimp-image-select-ellipse 1 0 200 150 200 200)' -b '(gimp-drawable-invert 1 1)' -b '(gimp-floating-sel-remove 1)' -b '(file-png-save-defaults 1 1 2 "wow" "rrr")' -b '(gimp-quit 0)'






















