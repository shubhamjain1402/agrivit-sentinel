"""
Nutrient Management Recommendations System
Author: Shubham Jain
Purpose: Provide detailed guidance on soil nutrient deficiency and excess management
Based on: Agricultural best practices and sustainable farming principles
"""

def get_nutrient_recommendations(nutrient_category):
    """
    Returns customized recommendations based on soil nutrient status
    
    Args:
        nutrient_category: One of 'excess_nitrogen', 'nitrogen_deficient', 
                          'excess_phosphorus', 'phosphorus_deficient', etc.
    
    Returns:
        Detailed HTML formatted recommendations
    """
    
    recommendations = {
        # ==================== NITROGEN MANAGEMENT ====================
        'excess_nitrogen': """
        <b style="color:#8B4513;">⚠ HIGH NITROGEN LEVELS DETECTED</b>
        <br/><br/>Excessive nitrogen promotes unwanted vegetative growth and may compromise crop quality.
        <br/><br/>
        <p align="justify"><b>Recommended Actions:</b></p>
        <p align="justify">
        <b>1. Adjust Fertilizer Application:</b> Switch to balanced NPK formulations with 
        lower nitrogen ratios (e.g., 5-10-10). Reduce nitrogen fertilizer frequency to allow soil 
        levels to normalize naturally through plant uptake and microbial processes.
        </p>
        <p align="justify">
        <b>2. Organic Matter Incorporation:</b> Add carbon-rich materials like aged sawdust, 
        wood chips, or straw to your soil. These materials immobilize excess nitrogen temporarily 
        as soil microorganisms decompose them, reducing bioavailable nitrogen for plants.
        </p>
        <p align="justify">
        <b>3. Crop Selection Strategy:</b> Plant nitrogen-demanding crops (tomatoes, corn, leafy 
        greens) that will utilize the excess nitrogen productively. These crops can typically handle 
        higher N levels without adverse effects.
        </p>
        <p align="justify">
        <b>4. Soil Leaching:</b> Controlled irrigation with deep watering helps mobilize nitrogen 
        beyond the root zone. However, use this method cautiously to avoid waterlogging and 
        nutrient loss to groundwater.
        </p>
        <p align="justify">
        <b>5. Mulching Practice:</b> Apply mulch (grass clippings, leaves, straw) to reduce soil 
        temperature and slow nitrogen mineralization from organic matter decomposition.
        </p>
        <hr style="height:2px; background-color:#8B4513;">
        """,
        
        'nitrogen_deficient': """
        <b style="color:#228B22;">⚠ LOW NITROGEN LEVELS DETECTED</b>
        <br/><br/>Nitrogen deficiency restricts plant protein synthesis and leads to stunted growth with yellowish leaves.
        <br/><br/>
        <p align="justify"><b>Recommended Actions:</b></p>
        <p align="justify">
        <b>1. Immediate Nitrogen Supplementation:</b> Apply nitrogen-rich fertilizers such as 
        urea (46% N), ammonium nitrate, or organic alternatives like fish emulsion. Follow label 
        instructions carefully and apply during active growing seasons for optimal uptake.
        </p>
        <p align="justify">
        <b>2. Legume Crop Rotation:</b> Plant nitrogen-fixing crops (beans, peas, clover, alfalfa) 
        in crop rotation sequences. These plants form symbiotic relationships with Rhizobium bacteria, 
        naturally replenishing soil nitrogen for subsequent crops.
        </p>
        <p align="justify">
        <b>3. Compost and Manure Application:</b> Incorporate well-aged compost or animal manure 
        (2-4 inches) into soil before planting. These organic inputs provide sustained nitrogen 
        release as soil organisms break them down gradually.
        </p>
        <p align="justify">
        <b>4. Green Manuring:</b> Plant nitrogen-fixing cover crops (hairy vetch, buckwheat) 
        and turn them into the soil before main crop planting. This enriches nitrogen levels 
        naturally without synthetic inputs.
        </p>
        <p align="justify">
        <b>5. Foliar Feeding:</b> Apply nitrogen foliar sprays (diluted fish emulsion or urea solution) 
        for quick nutrient absorption through leaves when soil deficiency is severe and plants need 
        immediate relief.
        </p>
        <hr style="height:2px; background-color:#228B22;">
        """,
        
        'nitrogen_balanced': """
        <b style="color:#2F4F4F;">✓ NITROGEN LEVELS OPTIMAL</b>
        <br/><br/>Your soil nitrogen content is well-suited for most crops. Maintain current levels 
        through balanced fertilization practices.
        <hr style="height:2px; background-color:#2F4F4F;">
        """,
        
        # ==================== PHOSPHORUS MANAGEMENT ====================
        'excess_phosphorus': """
        <b style="color:#8B4513;">⚠ HIGH PHOSPHORUS LEVELS DETECTED</b>
        <br/><br/>Excessive phosphorus reduces availability of micronutrients and causes 
        environmental pollution if it leaches into water systems.
        <br/><br/>
        <p align="justify"><b>Recommended Actions:</b></p>
        <p align="justify">
        <b>1. Minimize Phosphorus Fertilization:</b> Discontinue phosphorus-containing fertilizers 
        (avoid products with middle number greater than 0, e.g., 10-0-10). Use only 
        nitrogen-potassium fertilizers until soil P levels decline naturally.
        </p>
        <p align="justify">
        <b>2. Crop Rotation with Low-P Crops:</b> Grow crops that require minimal phosphorus 
        (grains, oats, barley) to gradually deplete soil reserves. Avoid phosphorus-demanding 
        crops like legumes and root vegetables.
        </p>
        <p align="justify">
        <b>3. Phosphorus Removal via Harvest:</b> Maximize crop yields to physically remove 
        phosphorus from soil through harvested biomass. More plant material removed = more soil 
        P exported off-farm.
        </p>
        <p align="justify">
        <b>4. Organic Matter Management:</b> Add carbon-rich materials that temporarily immobilize 
        phosphorus in microbial biomass, reducing plant-available P without permanent depletion.
        </p>
        <p align="justify">
        <b>5. pH Adjustment:</b> Lower soil pH slightly (6.0-6.5 range) through sulfur application. 
        Lower pH converts soluble phosphorus to less plant-available forms.
        </p>
        <hr style="height:2px; background-color:#8B4513;">
        """,
        
        'phosphorus_deficient': """
        <b style="color:#228B22;">⚠ LOW PHOSPHORUS LEVELS DETECTED</b>
        <br/><br/>Phosphorus deficiency impairs root development, flowering, and energy 
        metabolism in plants, reducing overall yield potential.
        <br/><br/>
        <p align="justify"><b>Recommended Actions:</b></p>
        <p align="justify">
        <b>1. Phosphate Fertilizer Application:</b> Use phosphorus-rich fertilizers such as 
        triple superphosphate, monoammonium phosphate (MAP), or diammonium phosphate (DAP). 
        Apply 50-150 lbs P₂O₅ per acre depending on soil test results.
        </p>
        <p align="justify">
        <b>2. Rock Phosphate/Bone Meal:</b> Apply slow-release phosphorus sources like rock phosphate 
        (150-500 lbs/acre) or bone meal (1,000-2,000 lbs/acre). These require microbial action for 
        conversion to available forms but provide long-term benefits.
        </p>
        <p align="justify">
        <b>3. Organic Compost Integration:</b> Incorporate 3-5 inches of quality compost containing 
        phosphorus-rich materials (bone meal, manure). Biological activity in compost enhances 
        phosphorus solubility.
        </p>
        <p align="justify">
        <b>4. Mycorrhizal Inoculant Application:</b> Introduce mycorrhizal fungi that form symbiotic 
        relationships with plant roots, dramatically increasing phosphorus uptake and utilization 
        efficiency.
        </p>
        <p align="justify">
        <b>5. pH Optimization:</b> Adjust soil pH to 6.0-7.0 range for maximum phosphorus 
        availability. Add lime if pH is too low, sulfur if too high.
        </p>
        <hr style="height:2px; background-color:#228B22;">
        """,
        
        'phosphorus_balanced': """
        <b style="color:#2F4F4F;">✓ PHOSPHORUS LEVELS OPTIMAL</b>
        <br/><br/>Phosphorus levels are adequate for crop production. Continue monitoring 
        through periodic soil tests.
        <hr style="height:2px; background-color:#2F4F4F;">
        """,
        
        # ==================== POTASSIUM MANAGEMENT ====================
        'excess_potassium': """
        <b style="color:#8B4513;">⚠ HIGH POTASSIUM LEVELS DETECTED</b>
        <br/><br/>Excessive potassium can interfere with magnesium and calcium absorption, 
        creating secondary nutrient deficiencies.
        <br/><br/>
        <p align="justify"><b>Recommended Actions:</b></p>
        <p align="justify">
        <b>1. Cease Potassium Fertilization:</b> Stop applying any potassium-containing fertilizers. 
        Select fertilizers with 0 as the third number (e.g., 10-10-0). Focus on nitrogen and 
        phosphorus applications only.
        </p>
        <p align="justify">
        <b>2. Deep Soil Leaching:</b> Apply controlled irrigation to move soluble potassium deeper 
        in the soil profile, reducing plant root access. Multiple irrigation cycles with drainage 
        help mobilize excess K downward.
        </p>
        <p align="justify">
        <b>3. Calcium and Magnesium Application:</b> Apply lime (CaCO₃) or magnesium sulfate 
        (Epsom salt) to provide competing cations that reduce potassium availability and correct 
        any secondary deficiencies.
        </p>
        <p align="justify">
        <b>4. Remove Potassium-Rich Materials:</b> Avoid adding manure, compost, or wood ash which 
        are potassium-rich. If using amendments, ensure they're K-poor.
        </p>
        <p align="justify">
        <b>5. Selective Crop Planting:</b> Grow low-potassium demanding crops (grains, cereals) 
        that won't exacerbate the imbalance.
        </p>
        <hr style="height:2px; background-color:#8B4513;">
        """,
        
        'potassium_deficient': """
        <b style="color:#228B22;">⚠ LOW POTASSIUM LEVELS DETECTED</b>
        <br/><br/>Potassium deficiency reduces plant stress tolerance, disease resistance, 
        and produces poor quality produce with shorter shelf life.
        <br/><br/>
        <p align="justify"><b>Recommended Actions:</b></p>
        <p align="justify">
        <b>1. Potassium Fertilizer Application:</b> Apply potassium sulfate or potassium chloride 
        at 100-200 lbs K₂O per acre. Broadcast over soil surface or incorporate pre-plant for 
        best results.
        </p>
        <p align="justify">
        <b>2. Organic Potassium Sources:</b> Use wood ash (5-20 lbs/1000 sq ft), kelp/seaweed 
        products, or greensand/glauconite. These provide K slowly as minerals break down.
        </p>
        <p align="justify">
        <b>3. Banana Peel Composting:</b> Bury dried banana peels 2-3 inches deep in planting areas. 
        As they decompose, potassium is released gradually into the root zone.
        </p>
        <p align="justify">
        <b>4. Compost and Manure Addition:</b> Incorporate 2-4 inches of aged manure or compost 
        (horse, chicken, rabbit manure) which contain significant potassium.
        </p>
        <p align="justify">
        <b>5. Foliar Supplementation:</b> Apply potassium foliar spray (potassium nitrate solution) 
        for quick uptake during growing season if deficiency symptoms appear.
        </p>
        <hr style="height:2px; background-color:#228B22;">
        """,
        
        'potassium_balanced': """
        <b style="color:#2F4F4F;">✓ POTASSIUM LEVELS OPTIMAL</b>
        <br/><br/>Potassium availability is excellent for healthy plant growth and development. 
        Maintain balance through regular monitoring.
        <hr style="height:2px; background-color:#2F4F4F;">
        """
    }
    
    return recommendations.get(nutrient_category, "No recommendations available for this category.")


# Legacy compatibility dictionary for existing code
fertilizer_dict = {
    'NHigh': get_nutrient_recommendations('excess_nitrogen'),
    'Nlow': get_nutrient_recommendations('nitrogen_deficient'),
    'NNo': get_nutrient_recommendations('nitrogen_balanced'),
    'PHigh': get_nutrient_recommendations('excess_phosphorus'),
    'Plow': get_nutrient_recommendations('phosphorus_deficient'),
    'PNo': get_nutrient_recommendations('phosphorus_balanced'),
    'KHigh': get_nutrient_recommendations('excess_potassium'),
    'Klow': get_nutrient_recommendations('potassium_deficient'),
    'KNo': get_nutrient_recommendations('potassium_balanced'),
}
