import bpy

# Set this to "True" if you want to reset bone names to their indexes.
reset = False


bone_dictionary = {
  "0000": "root",
  "0001": "root02",
  "0002": "rotation",
  "0003": "hip_rotation",
  "0004": "hips",
  "0005": "stomach",
  "0006": "neck",
  "0007": "head",

  # Spikes
  "0008": "spike_parent",
  "0009": "spikes01",
  "0010": "spikes02",
  "0011": "spikes03",
  "0012": "spike_front",
  
  # Knuckle's dreads
  "0013": "spike_l",
  "0014": "spike_r",

  # Cream's ears
  "0015": "c_ear01_r",
  "0016": "c_ear02_r",
  "0017": "c_ear03_r",

  "0018": "c_ear01_l",
  "0019": "c_ear02_l",
  "0020": "c_ear03_l",
  
  # Silver quills
  "0021": "s_spike_parent",
  "0022": "s_spike_r",
  "0023": "s_spike_l",
  "0024": "s_spike01",
  "0025": "s_spike02",

  
  # Faces
  "0026": "face_default",
  "0027": "face_shock",
  "0028": "face_happy",
  "0029": "face_sad",
  
  # Arm L
  "0030": "clavicle_l",
  "0031": "shoulder_l",
  "0032": "elbow_l",
  "0033": "wrist_l",
  "0034": "hand_open_l",
  "0035": "hand_flat_l",
  "0036": "hand_relax_l",
  "0037": "hand_fist_l",
  "0038": "hand_point_l",
  "0039": "hand_peace_l",
  "0040": "hand_thumb_l",
  "0041": "hand_curl_l",
  
  # Arm R
  "0042": "clavicle_r",
  "0043": "shoulder_r",
  "0044": "elbow_r",
  "0045": "wrist_r",
  "0046": "hand_open_r",
  "0047": "hand_flat_r",
  "0048": "hand_relax_r",
  "0049": "hand_fist_r",
  "0050": "hand_point_r",
  "0051": "hand_peace_r",
  "0052": "hand_thumb_r",
  "0053": "hand_curl_r",
  
  # Tails' tails
  "0054": "tail_parent",
  "0055": "tail01_l",
  "0056": "tail02_l",
  "0057": "tail03_l",
  "0058": "tail01_r",
  "0059": "tail02_r",
  "0060": "tail03_r",
  
  # Knuckles' tail
  "0061": "k_tail01",
  "0062": "k_tail02",
  "0063": "k_tail03",
  
  # Dress (Amy)
  "0064": "dress_parent",
  "0065": "dress_r",
  "0066": "dress_l",
  "0067": "dress_f",
  "0068": "dress_b",
  
  # Blaze coat
  "0069": "coat_parent",
  "0070": "coat01_r",
  "0071": "coat02_r",
  "0072": "coat01_l",
  "0073": "coat02_l",

  # Blaze's tail
  "0074": "b_tail_parent",
  "0075": "b_tail01",
  "0076": "b_tail02",
  "0077": "b_tail03",
  
  # Leg L
  "0078": "leg_l",
  "0079": "knee_l",
  "0080": "ankle_l",
  "0081": "toe_l",
  "0082": "toe_tip_l",
  
  # Leg R
  "0083": "leg_r",
  "0084": "knee_r",
  "0085": "ankle_r",
  "0086": "toe_r",
  "0087": "toe_tip_r",
  "0088": "root_attachment",
  "0089": "hand_attachment",
}


for obj in bpy.context.selected_objects:
    if obj.type != 'ARMATURE':
        continue

    bone_count = 0
    for bone in obj.pose.bones:
        bone_tokens = bone.name.split('_')
        bone_key = bone_tokens[len(bone_tokens) - 1]

        if reset:
            bone.name = "Bone_{:04}".format(bone_count)
        elif bone_key in bone_dictionary:
            bone.name = bone_dictionary.get(bone_key)
        
        bone_count += 1