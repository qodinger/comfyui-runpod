# Prompt Engineering Guide - Sharp Details & Quality Improvement

## Research Summary

Based on prompt engineering best practices for Stable Diffusion/ComfyUI, here are the key techniques for achieving sharp, detailed images:

### Key Principles:

1. **Prompt Structure**: Subject → Pose → Details → Quality Tags (in that order)
2. **Weighted Terms**: Use `(keyword:1.2)` to emphasize important elements
3. **Specific Descriptors**: Be precise about what you want (e.g., "M-shaped open legs" not just "open legs")
4. **Quality Tags Placement**: Put quality tags at the END for maximum impact
5. **Negative Prompts**: Comprehensive negative prompts reduce artifacts significantly

---

## Your Original Prompt Analysis

```
anime MILF, mature woman, beautiful face, big boobs, seductive expression, lie down, opened legs, show pussy, semen dripping from vagina, nude, explicit, tanned skin, tan skin, beauty mark on face, detailed anatomy, anatomically correct, soft skin, natural lighting, detailed face, masterpiece, best quality, ultra detailed, perfect anatomy, proper proportions --ar 16:9
```

### Issues Identified:

1. ❌ **Missing "goth" descriptor** - You want goth style but it's not mentioned
2. ❌ **Pose not specific enough** - "opened legs" should be "M-shaped open legs pose"
3. ❌ **Quality tags scattered** - Should be grouped at the end
4. ❌ **No weighted terms** - Important elements not emphasized
5. ❌ **Redundant terms** - "tanned skin, tan skin" is duplicate
6. ❌ **Lighting could be better** - "natural lighting" doesn't fit goth aesthetic

---

## Improved Prompt (Recommended)

### Version 1: Optimized for Sharp Details

```
goth MILF, gothic mature woman, dark gothic makeup, black lipstick, smoky eyes, pale skin with tanned undertones, beauty mark on cheek, long dark hair, gothic aesthetic,
lying down on bed, M-shaped open legs pose, legs spread wide in M-shape, knees bent outward, feet positioned wide apart,
nude, explicit, seductive expression, beautiful face, big breasts, full body visible,
show pussy, semen dripping from vagina, wet, glistening,
detailed anatomy, anatomically correct, perfect anatomy, proper body proportions, realistic proportions, natural body structure,
soft smooth skin, detailed skin texture, skin pores visible,
dramatic lighting, moody lighting, soft shadows, rim lighting, cinematic lighting,
detailed face, expressive eyes, detailed eyes, sharp eyes,
masterpiece, best quality, ultra detailed, highly detailed, 8k resolution, sharp focus, professional, detailed, perfect composition, beautiful, high quality,
anime style, professional anime art style, clean line art, vibrant colors,
(detailed anatomy:1.5), (sharp focus:1.4), (perfect anatomy:1.3), (detailed face:1.3), (M-shaped pose:1.2), (goth aesthetic:1.2)
--ar 16:9
```

### Version 2: More Concise (If Prompt Too Long)

```
goth MILF, gothic mature woman, dark gothic makeup, black lipstick, smoky eyes, tanned skin, beauty mark on cheek,
lying down, M-shaped open legs pose, legs spread wide, knees bent outward,
nude, explicit, seductive expression, beautiful face, big breasts,
show pussy, semen dripping from vagina,
detailed anatomy, anatomically correct, perfect anatomy, proper proportions,
soft skin, detailed skin texture,
dramatic moody lighting, soft shadows,
detailed face, expressive eyes,
masterpiece, best quality, ultra detailed, 8k resolution, sharp focus, professional,
anime style, professional anime art style,
(detailed anatomy:1.5), (sharp focus:1.4), (perfect anatomy:1.3), (M-shaped pose:1.2)
--ar 16:9
```

### Version 3: Maximum Quality (Longest, Most Detailed)

```
goth MILF, gothic mature woman, dark gothic aesthetic, gothic style,
dark gothic makeup, black lipstick, dark smoky eyes, heavy eyeliner, dark eyeshadow,
pale skin with tanned undertones, tanned complexion,
beauty mark on left cheek, beauty mark on face,
long dark hair, black hair, gothic hairstyle,
lying down on luxurious bed, reclining pose,
M-shaped open legs pose, legs spread wide in perfect M-shape, knees bent outward at 45 degrees, feet positioned wide apart, thighs spread,
nude, completely nude, explicit,
seductive expression, seductive look, seductive gaze,
beautiful face, attractive face, detailed face,
big breasts, large breasts, full breasts,
full body visible, complete body,
show pussy, visible pussy, exposed pussy,
semen dripping from vagina, cum dripping, wet, glistening,
detailed anatomy, anatomically correct, perfect anatomy, correct anatomy, natural anatomy,
proper body proportions, realistic proportions, natural body structure, correct body structure,
soft smooth skin, detailed skin texture, skin pores visible, realistic skin,
dramatic lighting, moody lighting, gothic lighting, soft shadows, rim lighting, cinematic lighting, chiaroscuro,
detailed face, expressive eyes, detailed eyes, sharp eyes, beautiful eyes,
masterpiece, best quality, ultra detailed, highly detailed, extremely detailed,
8k resolution, 4k resolution, sharp focus, professional, detailed,
perfect composition, beautiful, high quality,
anime style, professional anime art style, clean line art, vibrant colors,
(detailed anatomy:1.6), (sharp focus:1.5), (perfect anatomy:1.4), (detailed face:1.4), (M-shaped pose:1.3), (goth aesthetic:1.3), (sharp details:1.3), (skin texture:1.2)
--ar 16:9
```

---

## Key Improvements Explained

### 1. Added Goth Descriptors

- `goth MILF, gothic mature woman` - Establishes goth character
- `dark gothic makeup, black lipstick, smoky eyes` - Specific goth makeup
- `gothic aesthetic, gothic style` - Reinforces goth theme
- `dramatic moody lighting, gothic lighting` - Lighting that fits goth aesthetic

### 2. Enhanced Pose Description

- `M-shaped open legs pose` - Specific pose name
- `legs spread wide in M-shape` - Clear description
- `knees bent outward at 45 degrees` - Precise angle
- `feet positioned wide apart, thighs spread` - Complete pose description
- Weighted: `(M-shaped pose:1.2)` - Emphasizes the pose

### 3. Improved Sharpness Terms

- `sharp focus` - Direct sharpness term
- `8k resolution, 4k resolution` - High resolution tags
- `detailed skin texture, skin pores visible` - Texture detail
- `sharp eyes, detailed eyes` - Facial detail
- Weighted: `(sharp focus:1.4), (sharp details:1.3)` - Emphasizes sharpness

### 4. Better Anatomy Terms

- `anatomically correct, perfect anatomy, correct anatomy` - Multiple anatomy terms
- `proper body proportions, realistic proportions` - Proportion terms
- `natural body structure, correct body structure` - Structure terms
- Weighted: `(detailed anatomy:1.5), (perfect anatomy:1.3)` - Strong emphasis

### 5. Enhanced Lighting

- `dramatic lighting, moody lighting, gothic lighting` - Fits goth aesthetic
- `soft shadows, rim lighting, cinematic lighting` - Professional lighting
- `chiaroscuro` - Advanced lighting technique (high contrast)

### 6. Organized Structure

- **Subject** (goth MILF, appearance)
- **Pose** (M-shaped legs, position)
- **Content** (nude, explicit details)
- **Quality** (anatomy, proportions)
- **Details** (skin, lighting, face)
- **Quality Tags** (masterpiece, best quality, etc.)
- **Style** (anime style)
- **Weighted Terms** (emphasis)

### 7. Removed Redundancy

- Removed duplicate "tanned skin, tan skin" → kept "tanned skin"
- Consolidated quality tags at the end

---

## Prompt Engineering Best Practices Applied

### ✅ Weighted Terms

Use `(keyword:weight)` to emphasize important elements:

- `(detailed anatomy:1.5)` - 50% more emphasis on anatomy
- `(sharp focus:1.4)` - 40% more emphasis on sharpness
- `(perfect anatomy:1.3)` - 30% more emphasis on anatomy
- `(M-shaped pose:1.2)` - 20% more emphasis on pose

**Weight Guidelines:**

- 1.0 = normal emphasis
- 1.1-1.3 = light emphasis
- 1.4-1.6 = strong emphasis
- 1.7+ = very strong (use sparingly)

### ✅ Prompt Order Matters

Stable Diffusion processes prompts left-to-right, so:

1. **Subject** first (what you're generating)
2. **Pose/Position** (how they're positioned)
3. **Details** (specific features)
4. **Quality Tags** last (for maximum impact)

### ✅ Specificity

- ❌ "opened legs" → ✅ "M-shaped open legs pose, legs spread wide in M-shape"
- ❌ "natural lighting" → ✅ "dramatic moody lighting, gothic lighting, soft shadows"
- ❌ "detailed" → ✅ "detailed anatomy, detailed skin texture, detailed face"

### ✅ Quality Tag Placement

Quality tags work best at the END of the prompt:

```
...subject details..., masterpiece, best quality, ultra detailed, 8k resolution, sharp focus
```

### ✅ Negative Prompts

Your current negative prompt is good, but you can enhance it:

```
blurry, low quality, distorted, deformed, ugly, low resolution, pixelated, grainy, noisy,
bad anatomy, bad proportions, incorrect anatomy, wrong anatomy, malformed anatomy,
extra limbs, missing limbs, malformed hands, malformed feet,
extra fingers, missing fingers, fused fingers, too many fingers,
long neck, short neck, bad hands, bad feet, bad eyes,
twisted body, broken spine, unnatural joints, dislocated joints,
incorrect proportions, wrong proportions, disproportionate,
malformed genitals, distorted genitals,
multiple heads, multiple faces, double exposure, out of focus, motion blur,
bad composition, bad perspective, bad angle, awkward pose, unnatural pose,
watermark, text, signature, jpeg artifacts, compression artifacts,
oversaturated, undersaturated, low contrast, high contrast, dark, too bright,
bad lighting, bad shadows, harsh shadows, flat lighting,
duplicate, mutation, mutated, cloned, floating limbs, disconnected limbs
```

---

## Testing Recommendations

### Step 1: Test Base Prompt

Start with Version 2 (concise) to see if it generates correctly.

### Step 2: Add Weighted Terms

If results are good but need more emphasis, add weighted terms:

```
(detailed anatomy:1.5), (sharp focus:1.4), (perfect anatomy:1.3)
```

### Step 3: Refine Based on Results

- **Too blurry?** → Increase `(sharp focus:1.4)` to `(sharp focus:1.6)`
- **Bad anatomy?** → Increase `(detailed anatomy:1.5)` to `(detailed anatomy:1.7)`
- **Pose wrong?** → Increase `(M-shaped pose:1.2)` to `(M-shaped pose:1.4)`
- **Not goth enough?** → Add more goth descriptors at the beginning

### Step 4: Test Different Seeds

Try seeds: `-1` (random), `12345`, `67890`, `11111` to find best results.

---

## Advanced Techniques

### 1. Prompt Chaining

Break complex prompts into parts:

```
[goth MILF, gothic mature woman, dark gothic makeup]
[lying down, M-shaped open legs pose, legs spread wide]
[detailed anatomy, perfect anatomy, proper proportions]
[masterpiece, best quality, ultra detailed, 8k resolution, sharp focus]
```

### 2. Style Mixing

Combine styles for unique results:

```
goth MILF, gothic mature woman, (anime style:1.2), (realistic proportions:1.1)
```

### 3. Emphasis Brackets

Use `()` for light emphasis, `[]` for de-emphasis (if supported):

```
goth MILF, (detailed anatomy:1.5), [blurry:0.8]
```

### 4. Negative Prompt Weighting

Some models support negative prompt weighting:

```
Negative: (blurry:1.5), (bad anatomy:1.3), (low quality:1.2)
```

---

## Model-Specific Notes

### AnythingXL (Your Current Model)

- ✅ Responds well to detailed prompts
- ✅ Good with anatomy terms
- ✅ Works well with weighted terms
- ✅ Prefers specific descriptors over vague ones

### Recommended Settings for AnythingXL:

- **Steps**: 30-40 (you're using 30 ✅)
- **CFG Scale**: 7-8 (you're using 7.5 ✅)
- **Sampler**: `euler_ancestral` (you're using this ✅)
- **Scheduler**: `karras` (you're using this ✅)

---

## Final Recommended Prompt

**For best results, use this optimized version:**

```
goth MILF, gothic mature woman, dark gothic makeup, black lipstick, smoky eyes, tanned skin, beauty mark on cheek, long dark hair, gothic aesthetic,
lying down on bed, M-shaped open legs pose, legs spread wide in M-shape, knees bent outward, feet positioned wide apart,
nude, explicit, seductive expression, beautiful face, big breasts, full body visible,
show pussy, semen dripping from vagina, wet, glistening,
detailed anatomy, anatomically correct, perfect anatomy, proper body proportions, realistic proportions, natural body structure,
soft smooth skin, detailed skin texture,
dramatic moody lighting, gothic lighting, soft shadows, rim lighting,
detailed face, expressive eyes, detailed eyes, sharp eyes,
masterpiece, best quality, ultra detailed, highly detailed, 8k resolution, sharp focus, professional, detailed, perfect composition, beautiful, high quality,
anime style, professional anime art style, clean line art, vibrant colors,
(detailed anatomy:1.5), (sharp focus:1.4), (perfect anatomy:1.3), (detailed face:1.3), (M-shaped pose:1.2), (goth aesthetic:1.2)
--ar 16:9
```

**Expected Improvements:**

- ✅ Sharper details (sharp focus, 8k resolution, detailed texture)
- ✅ Better anatomy (weighted anatomy terms)
- ✅ Correct pose (specific M-shaped description)
- ✅ Goth aesthetic (goth descriptors + gothic lighting)
- ✅ Better composition (organized prompt structure)

---

## Troubleshooting

### If images are still blurry:

1. Increase `(sharp focus:1.4)` to `(sharp focus:1.6)`
2. Add `crisp details, sharp details, high definition`
3. Check image resolution (should be 1344x768 for 16:9)

### If anatomy is wrong:

1. Increase `(detailed anatomy:1.5)` to `(detailed anatomy:1.7)`
2. Add more anatomy terms: `correct anatomy, natural anatomy, anatomically correct`
3. Enhance negative prompt with more anatomy errors

### If pose is incorrect:

1. Increase `(M-shaped pose:1.2)` to `(M-shaped pose:1.4)`
2. Add more pose descriptors: `knees bent outward at 45 degrees, thighs spread wide`
3. Try different seeds to find better pose generation

### If not goth enough:

1. Add more goth descriptors at the beginning
2. Enhance lighting: `gothic lighting, dramatic shadows, moody atmosphere`
3. Add goth style terms: `gothic fashion, dark aesthetic, gothic style`

---

## References

- Stable Diffusion Prompt Engineering Best Practices
- ComfyUI/AnythingXL Model Documentation
- Prompt Weighting Techniques
- Anatomy Correction in AI Image Generation
- Sharp Detail Enhancement Methods

---

**Last Updated:** 2025-01-28
**Version:** 1.0
