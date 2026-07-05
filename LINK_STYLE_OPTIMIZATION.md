# Link Style Optimization

## Changes Made

### CSS Updates (`assets/css/_custom.scss`)

**Target:** About and Links pages only (not affecting post content)

**Selector:** `article.page.single .content p a, article.page.single .content li a`

### Default State
- **Color:** Inherit from text (no color change)
- **Underline:** 1px dashed border-bottom (using `currentColor`)
- **Opacity:** 0.85 (slightly faded)
- **Spacing:** 1px padding-bottom

### Hover State
- **Color:** Changes to theme accent color
- **Underline:** Changes to solid line
- **Border Color:** Changes to accent color
- **Opacity:** 1.0 (fully opaque)
- **Transition:** 0.25s smooth animation

## Generated CSS

```css
article.page.single .content p a,
article.page.single .content li a {
  color: inherit !important;
  text-decoration: none !important;
  border-bottom: 1px dashed currentColor;
  padding-bottom: 1px;
  opacity: 0.85;
  transition: all 0.25s ease;
}

article.page.single .content p a:hover,
article.page.single .content li a:hover {
  color: var(--accent-color) !important;
  border-bottom-color: var(--accent-color) !important;
  border-bottom-style: solid !important;
  opacity: 1;
}
```

## Testing

```bash
# Clean build
rm -rf public/ resources/ && hugo

# Start server
hugo server

# Test pages
http://localhost:1313/about/
http://localhost:1313/links/

# Clear browser cache: Ctrl+Shift+R
```

## Expected Behavior

1. **Email link:** `cryp71csec@gmail.com`
   - Default: Black text with dashed underline (slightly faded)
   - Hover: Accent color with solid underline (full opacity)

2. **GitHub link:** `https://github.com/L1nq0`
   - Default: Black text with dashed underline (slightly faded)
   - Hover: Accent color with solid underline (full opacity)

3. **Links page resources:**
   - All links follow the same pattern

## Notes

- Using `!important` to override theme default styles
- Using `border-bottom` instead of `text-decoration` for better visual control
- Only affects `<p>` and `<li>` links (excludes heading anchors)
- Dashed line uses `currentColor` to match text color
- Smooth 0.25s transition for professional feel
