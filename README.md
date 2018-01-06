The smartBot is chat bot that can learn facts that the user inputs and makes inferences based what it knows. 

Phrases that the smartBot can learn are in the following format. 

-  (A/An) <X> is (not) (a/an) <Y>  and  <X> are (not) <Y>
   Ex. "A dog is a canine"   "Dogs are canines?"  "Roofus is a dog"

   The smartBot will store this fact in its knowledge base. It will not matter whether the user enters their        response in singular or plural form. 
   
   The smartBot will respond "Got it" if the fact is new, and "I know" if that fact already exists in the          knowledge base.    


-  Is (a/an) <X> (a/an) <Y>?  and  Are <X> <Y>?
   Ex. "Is a dog a canine?"   "Are dogs canines?"

   The smartBot will answer the question with "Yes" if the fact is true, "No" if it is false, and "I'm not sure    given what you've told me so far" if it does not know based on what you've told it.

   Even if it wasn't explicitly told the answer, the smartBot will be able to draw on inferences to answer the      question. For instance, if you told it "Dogs are canines" and "Canines are hairy", it will know that "Dogs      are Hairy"
   
   It will not matter whether the user enters their question in singular or plural form. 
   
   
-  What do you know about <X>?
   Ex. "What do you know about dogs?"

   The smartBot will respond with all facts and inferences it can draw from its knowledge base about X. 


-  Other statements
   The smartBot will respond "I don't understand" to any statement not in one of the above formats


Below is a sample conversation about how the smartBot will work
