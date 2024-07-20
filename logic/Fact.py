class Fact:
    def __init__(self, fact, textual_explanation, visual_explanation, chase_explanation, is_for_chase, reasoning_task_id, knowledge_graph_id):
        self.fact = fact
        self.textual_explanation = textual_explanation
        self.visual_explanation = visual_explanation
        self.chase_explanation = chase_explanation
        self.is_for_chase = is_for_chase
        self.reasoning_task_id = reasoning_task_id
        self.knowledge_graph_id = knowledge_graph_id
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            fact=data['fact'],
            textual_explanation=data['textualExplanation'],
            visual_explanation=data['visualExplanation'],
            chase_explanation=data['chaseExplanation'],
            is_for_chase=data['isForChase'],
            reasoning_task_id=data['reasoningTaskId'],
            knowledge_graph_id=data['knowledgeGraphId']
        )
    
    def to_dict(self):
        """Converts the object to a dictionary suitable for JSON serialization."""
        return {
            'fact': self.fact,
            'textualExplanation': self.textual_explanation,
            'visualExplanation': self.visual_explanation,
            'chaseExplanation': self.chase_explanation,
            'isForChase': self.is_for_chase,
            'reasoningTaskId': self.reasoning_task_id,
            'knowledgeGraphId': self.knowledge_graph_id
        }
