# -*- coding: utf-8 -*-
"""
generate_aws_41_brain_functions_pdf.py
Builds a visually engaging, intuitive, graphical, and fun PDF developer guide:
'The AWS Developer's Field Guide: 41 Brain Functions on AWS'
Targeting Amazon Bedrock, DynamoDB, Step Functions, EventBridge, OpenSearch, Lambda, and SNS.
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding='utf-8')

PDF_PATH = r"c:\Users\richa\ai-engineering\AWS_41_Brain_Functions_Developer_Guide.pdf"

# PALETTE
C_NAVY = colors.HexColor("#0B132B")
C_BLUE = colors.HexColor("#1C2541")
C_ACCENT = colors.HexColor("#4F46E5")
C_AWS_ORANGE = colors.HexColor("#FF9900")
C_AWS_DARK = colors.HexColor("#232F3E")
C_PURPLE = colors.HexColor("#7C3AED")
C_EMERALD = colors.HexColor("#059669")
C_DANGER = colors.HexColor("#DC2626")
C_GOLD = colors.HexColor("#D97706")
C_BG_CARD = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#E2E8F0")
C_TEXT_DARK = colors.HexColor("#0F172A")
C_TEXT_MUTED = colors.HexColor("#475569")
C_CODE_BG = colors.HexColor("#0F172A")
C_CODE_TEXT = colors.HexColor("#F8FAFC")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top banner line
        self.setStrokeColor(C_AWS_ORANGE)
        self.setLineWidth(3)
        self.line(36, 756, 576, 756)

        # Header Text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(C_AWS_DARK)
        self.drawString(36, 762, "AWS COGNITIVE ARCHITECTURE FIELD GUIDE")
        self.setFont("Helvetica", 8)
        self.setFillColor(C_TEXT_MUTED)
        self.drawRightString(576, 762, "41 Brain Functions -> Amazon Web Services")

        # Bottom footer line
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(1)
        self.line(36, 38, 576, 38)

        # Footer Text
        self.setFont("Helvetica", 8)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(36, 26, "Amazon Bedrock • Step Functions • DynamoDB • EventBridge • Lambda")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 26, page_str)
        self.restoreState()

def create_guide_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=32,
        rightMargin=32,
        topMargin=34,
        bottomMargin=34
    )

    styles = getSampleStyleSheet()

    # CUSTOM STYLES
    s_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=26,
        textColor=C_AWS_DARK
    )
    s_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=C_TEXT_MUTED
    )
    s_h1 = ParagraphStyle(
        'PillarH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=C_AWS_DARK,
        spaceAfter=2
    )
    s_h2 = ParagraphStyle(
        'FunctionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=C_NAVY
    )
    s_badge = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )
    s_body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=C_TEXT_DARK
    )
    s_body_muted = ParagraphStyle(
        'BodyMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=C_TEXT_MUTED
    )
    s_code = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.2,
        textColor=C_CODE_TEXT
    )

    story = []

    # =========================================================================
    # FUNCTION BOX BUILDER HELPER
    # =========================================================================
    def build_function_row(fn_name, cat_type, badge_color, aws_svc, bio_desc, code_snippet, tip_text):
        content = [
            Paragraph(f"<b>{fn_name}</b> <font size=7.5 color='{badge_color}'>[{cat_type}]</font> &bull; <b>AWS:</b> {aws_svc}", s_h2),
            Paragraph(f"<i>Bio:</i> {bio_desc}", s_body_muted),
            Table([[Paragraph(f"<font color='#38BDF8'># AWS Implementation &bull; {aws_svc}</font><br/>{code_snippet}", s_code)]],
                  colWidths=[548],
                  style=[
                      ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
                      ('PADDING', (0,0), (-1,-1), 2.5),
                      ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
                  ]),
            Paragraph(f"<b>Builder Tip:</b> {tip_text}", s_body_muted),
            Spacer(1, 2)
        ]
        return content

    # =========================================================================
    # PAGE 1: COVER & ARCHITECTURE ROSETTA STONE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>The AWS Developer's Field Guide to 41 Brain Functions</b>", s_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Building Biological Cognitive Architecture with Amazon Bedrock, DynamoDB, Step Functions &amp; EventBridge", s_subtitle))
    story.append(Spacer(1, 12))

    # 5 CLASSIFICATION STATS BOXES
    stats_data = [
        [
            Paragraph("<font size=13><b>21</b></font><br/><b>REACTIVE</b><br/><font size=7 color='#1E40AF'>Responds After</font>", s_badge),
            Paragraph("<font size=13><b>7</b></font><br/><b>PROACTIVE</b><br/><font size=7 color='#6B21A8'>Acts Before (+)</font>", s_badge),
            Paragraph("<font size=13><b>1</b></font><br/><b>PARTLY</b><br/><font size=7 color='#075985'>Metacognition</font>", s_badge),
            Paragraph("<font size=13><b>7</b></font><br/><b>NOT YET</b><br/><font size=7 color='#374151'>Currently Lacking</font>", s_badge),
            Paragraph("<font size=13><b>5</b></font><br/><b>RESEARCH</b><br/><font size=7 color='#92400E'>Science Studying (?)</font>", s_badge),
        ]
    ]
    t_stats = Table(stats_data, colWidths=[108, 108, 108, 108, 108])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#DBEAFE")),
        ('TEXTCOLOR', (0,0), (0,0), colors.HexColor("#1E3A8A")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#F3E8FF")),
        ('TEXTCOLOR', (1,0), (1,0), colors.HexColor("#581C87")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#E0F2FE")),
        ('TEXTCOLOR', (2,0), (2,0), colors.HexColor("#0C4A6E")),
        ('BACKGROUND', (3,0), (3,0), colors.HexColor("#F3F4F6")),
        ('TEXTCOLOR', (3,0), (3,0), colors.HexColor("#1F2937")),
        ('BACKGROUND', (4,0), (4,0), colors.HexColor("#FEF3C7")),
        ('TEXTCOLOR', (4,0), (4,0), colors.HexColor("#78350F")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 1, C_BORDER),
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 14))

    # ROSETTA STONE SUMMARY TABLE
    story.append(Paragraph("<b>The Biological-to-AWS Cloud Mapping (The Rosetta Stone)</b>", s_h2))
    story.append(Spacer(1, 4))
    rosetta_data = [
        [
            Paragraph("<b>Cognitive Pillar</b>", s_body),
            Paragraph("<b>Biological Region</b>", s_body),
            Paragraph("<b>AWS Service Primitive</b>", s_body),
            Paragraph("<b>Developer Implementation Hook</b>", s_body)
        ],
        [
            Paragraph("<b>1. PERCEIVE &amp; ATTEND</b>", s_body),
            Paragraph("Thalamus, Superior Colliculus", s_body_muted),
            Paragraph("<b>Amazon EventBridge + Kinesis</b>", s_body),
            Paragraph("Rule-based content filtering &amp; token streaming", s_body_muted)
        ],
        [
            Paragraph("<b>2. REMEMBER</b>", s_body),
            Paragraph("Hippocampus, Neocortex", s_body_muted),
            Paragraph("<b>DynamoDB + OpenSearch Serverless</b>", s_body),
            Paragraph("TTL auto-expiry (Forgetting) &amp; Vector k-NN (Episodic)", s_body_muted)
        ],
        [
            Paragraph("<b>3. THINK &amp; DECIDE</b>", s_body),
            Paragraph("Frontopolar (BA 10), ACC", s_body_muted),
            Paragraph("<b>AWS Bedrock + Step Functions</b>", s_body),
            Paragraph("Tool calling, Guardrails veto &amp; DAG State Machines", s_body_muted)
        ],
        [
            Paragraph("<b>4. LEARN &amp; FEEL</b>", s_body),
            Paragraph("Amygdala, VTA Dopamine", s_body_muted),
            Paragraph("<b>Amazon CloudWatch + Model Eval</b>", s_body),
            Paragraph("Urgency metric alarms &amp; RPE feedback loops", s_body_muted)
        ],
        [
            Paragraph("<b>5. ACT &amp; REGULATE</b>", s_body),
            Paragraph("Motor M1, Cerebellum, Insula", s_body_muted),
            Paragraph("<b>AWS Lambda + Service Quotas</b>", s_body),
            Paragraph("Action execution, token bucket rate dampening", s_body_muted)
        ],
        [
            Paragraph("<b>6. CONNECT &amp; AWARE</b>", s_body),
            Paragraph("Corpus Callosum, GWT Bus", s_body_muted),
            Paragraph("<b>Amazon SNS + ElastiCache Redis</b>", s_body),
            Paragraph("Conscious blackboard fanout &amp; Evidence Voting", s_body_muted)
        ]
    ]
    t_rosetta = Table(rosetta_data, colWidths=[130, 110, 150, 150])
    t_rosetta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_rosetta)
    story.append(Spacer(1, 14))

    # INTRODUCTORY TIP BOX
    intro_box = [
        [Paragraph("<b>💡 The Cloud Architecture Insight:</b> The human brain is not a monolith—it is a distributed event-driven multi-agent system. In AWS, you do not build a 41-function brain in a single prompt. You build it by orchestrating specialized serverless primitives: <b>EventBridge</b> as the Thalamus, <b>DynamoDB</b> as the Hippocampus, <b>Bedrock</b> as the Prefrontal Cortex, and <b>SNS/Redis</b> as the Global Workspace conscious blackboard.", s_body)]
    ]
    t_intro = Table(intro_box, colWidths=[540])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (0,0), 1, C_AWS_ORANGE),
        ('PADDING', (0,0), (0,0), 8),
    ]))
    story.append(t_intro)

    # =========================================================================
    # PAGE 2: PILLAR 1 — PERCEIVE & ATTEND (7 FUNCTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>Pillar 1: PERCEIVE &amp; ATTEND (7 Functions)</b>", s_h1))
    story.append(Paragraph("Sensory gating, attention allocation, prediction error calculation, and spatiotemporal navigation.", s_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8, spaceBefore=4))

    # 1. Perception
    fn1 = build_function_row(
        "+ Perception", "PROACTIVE (+)", "#7C3AED", "Amazon EventBridge Rule Filtering",
        "Thalamic pre-attentive sensory intake filtering 99% of ambient noise before cortex.",
        "eventbridge = boto3.client('events')<br/>"
        "rule = eventbridge.put_rule(Name='ThalamicPerceptionGate',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;EventPattern=json.dumps({'detail': {'severity': ['HIGH', 'CRITICAL'], 'entropy': [{'numeric': ['&gt;', 0.85]}]}}))",
        "Filters telemetry before invoking LLM inference, preventing token flooding and cost explosion."
    )
    for el in fn1: story.append(el)

    # 2. Selective Attention
    fn2 = build_function_row(
        "Selective Attention", "REACTIVE", "#2563EB", "Bedrock Dynamic Context Window Masking",
        "Parieto-frontal network directing high-resolution processing onto salient tokens.",
        "bedrock = boto3.client('bedrock-runtime')<br/>"
        "response = bedrock.converse(modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;messages=[{'role':'user', 'content': [{'text': f'&lt;focus&gt;{focal_incident}&lt;/focus&gt; Ignore distractors: {noisy_logs}'}]}],<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;inferenceConfig={'temperature': 0.1, 'topP': 0.9})",
        "Use XML tags &lt;focus&gt; in Bedrock Converse API to create an artificial attention hotspot."
    )
    for el in fn2: story.append(el)

    # 3. Inhibition of Return
    fn3 = build_function_row(
        "Inhibition of Return", "REACTIVE", "#2563EB", "DynamoDB Visited Path Anti-Loop Cache",
        "Superior colliculus bias suppressing recently evaluated failure coordinates.",
        "dynamodb = boto3.resource('dynamodb').Table('AgentVisitedCoords')<br/>"
        "dynamodb.put_item(Item={'path_hash': node_hash, 'visited_at': int(time.time()), 'ttl': int(time.time() + 300)})<br/>"
        "candidate_paths = [p for p in next_steps if not dynamodb.get_item(Key={'path_hash': p.hash}).get('Item')]",
        "Attaches short TTL items to DynamoDB so agents never repeat a failed tool execution branch."
    )
    for el in fn3: story.append(el)

    # 4. Multisensory
    fn4 = build_function_row(
        "Multisensory", "NOT YET", "#64748B", "Amazon Bedrock Multi-Modal Converse API",
        "Superior temporal sulcus binding audio, visual, and symbolic signals into unified percepts.",
        "bedrock.converse(modelId='anthropic.claude-3-5-sonnet-20241022-v2:0', messages=[{'role':'user', 'content': [<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;{'image': {'format': 'png', 'source': {'bytes': screenshot_bytes}}},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;{'text': f'Correlate OCR error with audio transcript: {audio_text} and syslogs'}]}])",
        "Pass multi-modal arrays directly in Bedrock Converse API to achieve multimodal sensory binding."
    )
    for el in fn4: story.append(el)

    # 5. Spatial Navigation
    fn5 = build_function_row(
        "Spatial Navigation", "NOT YET", "#64748B", "Amazon Neptune Graph / OpenSearch 3D k-NN",
        "Hippocampal grid &amp; place cells building 3D topological cognitive maps.",
        "neptune_client.execute_gremlin_query(<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'g.V().hasLabel(\"Microservice\").has(\"id\", source).repeat(out().simplePath()).until(has(\"id\", target)).path()')",
        "Treat cloud infrastructure topologies as a cognitive spatial graph to navigate failure nodes."
    )
    for el in fn5: story.append(el)

    # 6. Time Perception
    fn6 = build_function_row(
        "Time Perception", "NOT YET", "#64748B", "AWS Step Functions Countdown Timers",
        "Striatal beat frequency &amp; cerebellar clocks tracking subjective duration and SLA deadlines.",
        "step_function_state = {<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Type': 'Wait', 'SecondsPath': '$.sla_remaining_seconds',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Next': 'EvaluateSlaBreachPenalty'}",
        "LLMs have no internal clock; Step Functions Wait states provide biological temporal pacing."
    )
    for el in fn6: story.append(el)

    # 7. Predictive Coding
    fn7 = build_function_row(
        "? Predictive Coding", "RESEARCH (?)", "#D97706", "Bedrock Token Logprobs Surprise Entropy",
        "Hierarchical Bayesian predictive modeling where top-down expectations cancel sensory noise.",
        "# Calculate Shannon surprise: surprise = -log(prob_predicted)<br/>"
        "if token_surprise &gt; SURPRISE_THRESHOLD:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;trigger_hierarchical_belief_update(event)",
        "Use token logprobs from model completions to calculate epistemic surprise and trigger recalculation."
    )
    for el in fn7: story.append(el)

    # =========================================================================
    # PAGE 3: PILLAR 2 — REMEMBER (7 FUNCTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>Pillar 2: REMEMBER (7 Functions)</b>", s_h1))
    story.append(Paragraph("Working memory, episodic retrieval, consolidation, associative memory, and principled forgetting.", s_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8, spaceBefore=4))

    # 8. Working Memory
    fn8 = build_function_row(
        "Working Memory", "REACTIVE", "#2563EB", "Amazon ElastiCache Redis / DynamoDB Session Buffer",
        "Dorsolateral PFC holding active variables online across short computational delays.",
        "redis_client.setex(f'agent:wm:{session_id}', 120, json.dumps({'active_bindings': {'uid': '4091', 'state': 'HELD'}}))<br/>"
        "active_vars = json.loads(redis_client.get(f'agent:wm:{session_id}'))['active_bindings']",
        "Sub-millisecond Redis keys represent active prefrontal working memory buffers."
    )
    for el in fn8: story.append(el)

    # 9. Episodic Memory
    fn9 = build_function_row(
        "Episodic Memory", "REACTIVE", "#2563EB", "Amazon OpenSearch Serverless Vector k-NN",
        "Hippocampal autoassociative network indexing unique spatio-temporal autobiographical events.",
        "opensearch_client.search(index='agent_episodes', body={<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'query': {'knn': {'episode_vector': {'vector': embedding, 'k': 5}}},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'post_filter': {'range': {'timestamp': {'gte': 'now-30d'}}}})",
        "Add timestamp metadata filters to vector k-NN queries to mirror human episodic recency."
    )
    for el in fn9: story.append(el)

    # 10. Consolidation
    fn10 = build_function_row(
        "Consolidation", "REACTIVE", "#2563EB", "EventBridge Cron + Lambda Batch Compaction to S3",
        "Slow-wave sleep transfer from fragile hippocampus into permanent neocortical schemas.",
        "# Scheduled Lambda runs nightly to compress conversational turn buffers into enduring markdown runbooks<br/>"
        "s3.put_object(Bucket='neocortical-schemas', Key=f'schemas/{date}.json', Body=consolidated_schema_json)",
        "Synthesize daily session logs into high-level declarative knowledge schemas before purging raw traces."
    )
    for el in fn10: story.append(el)

    # 11. Associative Memory
    fn11 = build_function_row(
        "Associative Memory", "REACTIVE", "#2563EB", "Amazon Bedrock Titan Embeddings Cosine Similarity",
        "Hopfield-like content-addressable recall reconstructing full patterns from sparse noisy cues.",
        "bedrock.invoke_model(modelId='amazon.titan-embed-text-v2:0',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;body=json.dumps({'inputText': 'that database outage with split-brain Raft in Singapore'}))",
        "Dense vector proximity performs Hopfield pattern completion from fragmentary human cues."
    )
    for el in fn11: story.append(el)

    # 12. Skill Memory
    fn12 = build_function_row(
        "Skill Memory", "REACTIVE", "#2563EB", "Amazon Bedrock Action Groups / OpenAPI Tool Registries",
        "Basal ganglia procedural memory executing automated habits without deliberation.",
        "bedrock_agent.create_agent_action_group(agentId=agent_id, actionGroupName='DevOpsSkills',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;apiSchema={'s3': {'s3BucketName': 'agent-skills', 's3ObjectKey': 'openapi-schema.json'}},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;actionGroupExecutor={'lambda': 'arn:aws:lambda:us-east-1:123456789012:function:SkillRunner'})",
        "Compiled OpenAPI schemas represent executable motor/cognitive skills in Bedrock Agents."
    )
    for el in fn12: story.append(el)

    # 13. Forgetting
    fn13 = build_function_row(
        "Forgetting", "NOT YET", "#64748B", "Amazon DynamoDB Native TTL Auto-Expiry Policy",
        "Active synaptic pruning, microglia degradation, and logarithmic Ebbinghaus decay.",
        "# DynamoDB automatically prunes items when current epoch exceeds ttl_epoch<br/>"
        "dynamodb.update_time_to_live(TableName='EpisodicBuffer',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;TimeToLiveSpecification={'Enabled': True, 'AttributeName': 'ebbinghaus_expire_epoch'})",
        "Never hoard infinite context. Configure DynamoDB TTL to simulate biological forgetting."
    )
    for el in fn13: story.append(el)

    # 14. Reconsolidation
    fn14 = build_function_row(
        "? Reconsolidation", "RESEARCH (?)", "#D97706", "DynamoDB Conditional Update Expression",
        "Recalled memories become temporarily labile and safely update without corruption.",
        "dynamodb.update_item(Key={'entity_id': 'customer_tier'},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;UpdateExpression='SET tier = :new_tier, last_reconsolidated = :now',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;ConditionExpression='version = :expected_version', ExpressionAttributeValues={':new_tier': 'DIAMOND'})",
        "Use optimistic locking (ConditionExpression) so agents update long-term beliefs without race conditions."
    )
    for el in fn14: story.append(el)

    # =========================================================================
    # PAGE 4: PILLAR 3 — THINK & DECIDE (8 FUNCTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>Pillar 3: THINK &amp; DECIDE (8 Functions)</b>", s_h1))
    story.append(Paragraph("Executive function, hierarchical planning, response inhibition, error monitoring, and reality monitoring.", s_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8, spaceBefore=4))

    # 15. Decision-making
    fn15 = build_function_row(
        "Decision-making", "REACTIVE", "#2563EB", "Bedrock Converse Tool Use &amp; JSON Routing",
        "Ventromedial PFC evaluating subjective expected utility across alternatives.",
        "response = bedrock.converse(modelId=MODEL_ID, messages=msgs, toolConfig={'tools': [<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;{'toolSpec': {'name': 'execute_failover', 'description': 'Promotes replica to master',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'inputSchema': {'json': {'type': 'object', 'properties': {'shard_id': {'type': 'string'}}}}}}]})",
        "Enforce strict JSON schemas in toolConfig to guarantee structured deterministic decision choices."
    )
    for el in fn15: story.append(el)

    # 16. Planning
    fn16 = build_function_row(
        "Planning", "REACTIVE", "#2563EB", "AWS Step Functions Hierarchical State Machine",
        "Frontopolar cortex (BA 10) orchestrating multi-step goal-subgoal dependency trees.",
        "sfn = boto3.client('stepfunctions')<br/>"
        "sfn.start_execution(stateMachineArn='arn:aws:states:us-east-1:123456789:stateMachine:AgentPlanningDAG',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;input=json.dumps({'goal': 'migrate_database', 'checkpoints': ['preflight', 'backup', 'cutover']}))",
        "Decompose complex agent plans into visual Step Functions workflows with automatic rollback states."
    )
    for el in fn16: story.append(el)

    # 17. Response Inhibition
    fn17 = build_function_row(
        "Response Inhibition", "REACTIVE", "#2563EB", "Amazon Bedrock Guardrails Veto Engine",
        "Right inferior frontal gyrus &amp; subthalamic nucleus aborting prepotent destructive actions.",
        "response = bedrock.converse(modelId=MODEL_ID, messages=msgs,<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;guardrailConfig={'guardrailIdentifier': 'gr-prod-safety-veto', 'guardrailVersion': 'DRAFT'})<br/>"
        "if response.get('stopReason') == 'guardrail_intervened': trigger_emergency_veto_alert()",
        "Bedrock Guardrails natively intercept and veto destructive actions before generation finishes."
    )
    for el in fn17: story.append(el)

    # 18. Error Monitoring
    fn18 = build_function_row(
        "Error Monitoring", "REACTIVE", "#2563EB", "AWS Step Functions Catch/Retry Block (ERN)",
        "Anterior cingulate cortex (ACC) generating Error-Related Negativity upon expectation mismatch.",
        "{'Type': 'Task', 'Resource': 'arn:aws:lambda:...:ValidateSyntax',<br/>"
        "&nbsp;'Catch': [{'ErrorEquals': ['SyntaxError', 'SchemaViolation'], 'ResultPath': '$.error_trace', 'Next': 'SelfCorrectionLoop'}]}",
        "Mimics biological ERN by catching syntax errors instantly and redirecting to a self-correction prompt."
    )
    for el in fn18: story.append(el)

    # 19. Reality Monitoring
    fn19 = build_function_row(
        "Reality Monitoring", "REACTIVE", "#2563EB", "AWS KMS Cryptographic Provenance Signatures",
        "Anterior PFC distinguishing real perceptual observations from self-generated internal thoughts.",
        "def verify_perceptual_provenance(item):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return kms.verify(KeyId=KMS_TELEMETRY_KEY, Message=item['raw_data'], Signature=item['sig'])['SignatureValid']",
        "Sign verified sensor/API telemetry with KMS. Anything unsigned is tagged as 'internal model thought'."
    )
    for el in fn19: story.append(el)

    # 20. Imagination
    fn20 = build_function_row(
        "Imagination", "REACTIVE", "#2563EB", "Bedrock High-Temperature Counterfactual Rollouts",
        "Default Mode Network simulating hypothetical futures and counterfactual rollouts.",
        "sim_reply = bedrock.converse(modelId=MODEL_ID, messages=[{'role': 'user', 'content': [{'text':<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Counterfactual rollout: What if us-east-1 loses DNS for 4 hours? Enumerate cascade failure points.'}]}],<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;inferenceConfig={'temperature': 0.85, 'maxTokens': 400})",
        "Increase temperature to 0.85+ on separate worker threads to generate creative contingency simulations."
    )
    for el in fn20: story.append(el)

    # 21. Prioritizing
    fn21 = build_function_row(
        "+ Prioritizing", "PROACTIVE (+)", "#7C3AED", "Amazon SQS Priority Queues / Message Weighting",
        "Prefrontal triage allocating scarce cognitive bandwidth to highest-impact threats.",
        "sqs.send_message(QueueUrl=CRITICAL_QUEUE_URL, MessageBody=json.dumps(incident_payload),<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;MessageAttributes={'ThreatSeverity': {'DataType': 'String', 'StringValue': 'P0_RANSOMWARE'}})",
        "Route critical threat messages to dedicated high-priority SQS FIFO queues before standard tasks."
    )
    for el in fn21: story.append(el)

    # 22. Flexibility
    fn22 = build_function_row(
        "+ Flexibility", "PROACTIVE (+)", "#7C3AED", "Step Functions Circuit Breaker Contingency Swap",
        "Orbitofrontal reversal learning dynamically repointing strategies when rewards invert.",
        "# Dynamic branching in Step Functions state machine<br/>"
        "{'Type': 'Choice', 'Choices': [{'Variable': '$.endpoint_status', 'NumericEquals': 500, 'Next': 'TriggerFallbackDAG'}], 'Default': 'ExecutePrimary'}",
        "Swap to asynchronous fallback DAGs instantly without crashing or restarting the agent session."
    )
    for el in fn22: story.append(el)

    # =========================================================================
    # PAGE 5: PILLAR 4 — LEARN & FEEL (6 FUNCTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>Pillar 4: LEARN &amp; FEEL (6 Functions)</b>", s_h1))
    story.append(Paragraph("Continuous learning, reward prediction error, somatic emotional markers, metacognition, and insight.", s_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8, spaceBefore=4))

    # 23. Learning
    fn23 = build_function_row(
        "+ Learning", "PROACTIVE (+)", "#7C3AED", "Amazon Bedrock Prompt Caching &amp; Continuous LoRA",
        "Hebbian synaptic plasticity and continuous experiential adaptation.",
        "# Store learned exemplars in Bedrock prompt cache checkpoints<br/>"
        "prompt_cache = bedrock.create_prompt_cache(modelId=MODEL_ID, prompt=f'Learned rules: {learned_rules}\\n{task_prompt}')",
        "Update cached system prompts with runtime corrections so models never repeat verified mistakes."
    )
    for el in fn23: story.append(el)

    # 24. Reward Learning
    fn24 = build_function_row(
        "Reward Learning", "NOT YET", "#64748B", "DynamoDB Dopamine Reward Prediction Error (RPE)",
        "VTA dopamine neurons calculating RPE delta (Actual Reward - Expected Reward).",
        "rpe_delta = actual_system_metric_gain - expected_utility<br/>"
        "dynamodb.update_item(Key={'policy_id': 'action_failover'},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;UpdateExpression='ADD policy_weight :delta', ExpressionAttributeValues={':delta': Decimal(str(rpe_delta))})",
        "Use mathematical RPE adjustments in DynamoDB to dynamically boost or demote tool calling probabilities."
    )
    for el in fn24: story.append(el)

    # 25. Emotion
    fn25 = build_function_row(
        "Emotion", "NOT YET", "#64748B", "Amazon CloudWatch Composite Metric Somatic Alarms",
        "Amygdala &amp; insular affective valuation tagging stimuli with somatic urgency and threat scores.",
        "cloudwatch.put_composite_alarm(AlarmName='SomaticPanicAlarm',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;AlarmRule='(ALARM(LedgerDiscrepancy) OR ALARM(HighMemoryLeak)) AND ALARM(CustomerImpact)',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;ActionsEnabled=True, AlarmActions=['arn:aws:sns:...:ThrottleNonEssentialTasks'])",
        "Emotions are somatic survival bounds. Use Composite CloudWatch alarms to throttle risk budgets."
    )
    for el in fn25: story.append(el)

    # 26. Metacognition
    fn26 = build_function_row(
        "Metacognition", "PARTLY (~1)", "#0284C7", "Bedrock Self-Calibration &amp; Epistemic Uncertainty",
        "Anterior PFC monitoring confidence, knowing what you do not know, and abstaining safely.",
        "prompt = 'Estimate confidence (0-100%). If confidence &lt; 85%, reply ABSTAIN_AND_ESCALATE with missing variables.'<br/>"
        "if parsed_confidence &lt; 0.85: return request_human_in_the_loop_approval(context)",
        "Prompt the model for verbalized epistemic confidence and enforce strict human-in-the-loop escalation."
    )
    for el in fn26: story.append(el)

    # 27. Insight (Aha!)
    fn27 = build_function_row(
        "? Insight (Aha!)", "RESEARCH (?)", "#D97706", "OpenSearch Lateral Associative Leaping",
        "Right anterior superior temporal gyrus sudden non-linear restructuring of the problem space.",
        "# Cross-domain vector search linking two completely unrelated document clusters<br/>"
        "query = {'query': {'hybrid': {'queries': [{'match': {'text': 'puzzle'}}, {'knn': {'vector': metaphor_vec}}]}}}",
        "Use hybrid lexical/vector queries across distant knowledge domains to discover non-linear associative solutions."
    )
    for el in fn27: story.append(el)

    # 28. Sleep & Memory
    fn28 = build_function_row(
        "? Sleep &amp; Memory", "RESEARCH (?)", "#D97706", "AWS EventBridge Scheduled Batch Rehearsal",
        "Hippocampal sharp-wave ripples replaying episodes at 10x speed to prevent catastrophic forgetting.",
        "# EventBridge triggers overnight Lambda: Replays previous day's edge cases into model fine-tuning or vector store<br/>"
        "events.put_rule(Name='HippocampalSleepReplayCron', ScheduleExpression='cron(0 3 * * ? *)')",
        "Run automated offline replay loops overnight to harden fragile short-term memories into permanent schemas."
    )
    for el in fn28: story.append(el)

    # =========================================================================
    # PAGE 6: PILLAR 5 — ACT & REGULATE (5 FUNCTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>Pillar 5: ACT &amp; REGULATE (5 Functions)</b>", s_h1))
    story.append(Paragraph("Motor tool execution, synaptic token streaming, lateral inhibition, and homeostatic self-regulation.", s_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8, spaceBefore=4))

    # 29. Motor Execution
    fn29 = build_function_row(
        "Motor Execution", "REACTIVE", "#2563EB", "AWS Lambda Tool Invocation via Action Groups",
        "Primary motor cortex (M1) and corticospinal tract sending physical/digital commands.",
        "lambda_client.invoke(FunctionName='ExecuteCloudCommand',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;InvocationType='RequestResponse', Payload=json.dumps({'command': 'aws ec2 reboot-instances', 'target': 'i-094'}))",
        "Every motor tool execution should run inside an isolated, permission-scoped AWS Lambda sandbox."
    )
    for el in fn29: story.append(el)

    # 30. Synaptic Signaling
    fn30 = build_function_row(
        "Synaptic Signaling", "REACTIVE", "#2563EB", "Amazon Bedrock ConverseStream Chunk Pipeline",
        "Action potentials releasing neurotransmitters across microscopic synaptic clefts.",
        "stream = bedrock.converse_stream(modelId=MODEL_ID, messages=msgs)<br/>"
        "for event in stream['stream']:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if 'contentBlockDelta' in event: emit_token_signal(event['contentBlockDelta']['delta']['text'])",
        "Use Bedrock ConverseStream to propagate continuous token activations into downstream microservices."
    )
    for el in fn30: story.append(el)

    # 31. Lateral Inhibition
    fn31 = build_function_row(
        "Lateral Inhibition", "REACTIVE", "#2563EB", "Bedrock Inference Top-P &amp; Temperature Tightening",
        "Interneurons sharpening contrast by inhibiting competing sub-threshold firing pathways.",
        "# Restrict TopP to 0.7 and Temperature to 0.05 to prune competing low-probability candidate tokens<br/>"
        "response = bedrock.converse(modelId=MODEL_ID, messages=msgs, inferenceConfig={'temperature': 0.05, 'topP': 0.7})",
        "Tighten TopP and Temperature parameters to suppress fuzzy hallucinatory noise and sharpen winner logits."
    )
    for el in fn31: story.append(el)

    # 32. Self-Regulation
    fn32 = build_function_row(
        "+ Self-Regulation", "PROACTIVE (+)", "#7C3AED", "AWS Service Quotas &amp; WAF Token Bucket Throttling",
        "Prefrontal-subcortical homeostatic regulation keeping effort and cost within safe bounds.",
        "waf = boto3.client('wafv2')<br/>"
        "# Enforce token bucket rate limiting on LLM agent endpoints to prevent runaway billing<br/>"
        "waf.update_rate_based_rule(RateKey='IP', Limit=100, Action={'Block': {}})",
        "Wrap all LLM agent loops with rate limiters and budget guardrails to prevent runaway compute storms."
    )
    for el in fn32: story.append(el)

    # 33. Interoception
    fn33 = build_function_row(
        "Interoception", "NOT YET", "#64748B", "Amazon CloudWatch Host Metric Self-Telemetry",
        "Insular cortex sensing internal physiological states (heart rate, temperature, glucose).",
        "metrics = cloudwatch.get_metric_data(MetricDataQueries=[<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;{'Id': 'vram', 'MetricStat': {'Metric': {'Namespace': 'AWS/ECS', 'MetricName': 'MemoryUtilization'}}},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;{'Id': 'tokens', 'MetricStat': {'Metric': {'Namespace': 'Bedrock', 'MetricName': 'Invocations'}}}])",
        "Agents must monitor their own memory utilization and token burn rates as internal somatic health metrics."
    )
    for el in fn33: story.append(el)

    # =========================================================================
    # PAGE 7: PILLAR 6 — CONNECT & AWARE (8 FUNCTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>Pillar 6: CONNECT &amp; AWARE (8 Functions)</b>", s_h1))
    story.append(Paragraph("Global Workspace broadcast, hemisphere transfer, evidence voting, and proactive ambient vigilance.", s_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8, spaceBefore=4))

    # 34. Connectivity
    fn34 = build_function_row(
        "Connectivity", "REACTIVE", "#2563EB", "Amazon EventBridge Custom Event Bus &amp; WebSockets",
        "White matter tracts connecting modular distributed brain regions.",
        "events.put_events(Entries=[{'Source': 'agent.security', 'DetailType': 'VulnerabilityFound',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Detail': json.dumps({'cve': 'CVE-2024-9042', 'target': 'shard-3'}), 'EventBusName': 'CognitiveBus'}])",
        "Use an EventBridge event bus as the high-throughput white matter highway connecting specialized agents."
    )
    for el in fn34: story.append(el)

    # 35. Hemisphere Transfer
    fn35 = build_function_row(
        "Hemisphere Transfer", "REACTIVE", "#2563EB", "Dual-Model Architecture (Claude 3.5 + Nova/Titan)",
        "Corpus callosum synchronizing analytic left-brain and holistic right-brain operations.",
        "# Left Hemisphere: Structured Symbolic Validator (Claude 3.5 Sonnet)<br/>"
        "# Right Hemisphere: Intuitive Creative Drafter (Amazon Nova Pro)<br/>"
        "draft = invoke_right_brain(prompt); final_verified = invoke_left_brain(draft)",
        "Pair an intuitive generator with a strict analytic validator to recreate corpus callosum balance."
    )
    for el in fn35: story.append(el)

    # 36. Global Workspace
    fn36 = build_function_row(
        "Global Workspace", "REACTIVE", "#2563EB", "Amazon SNS Fanout + Redis Shared Whiteboard (GWT)",
        "Baars &amp; Dehaene Global Workspace broadcasting essential facts across all modular agents in O(N).",
        "# Broadcast critical conscious state update to all subscribing specialized agents simultaneously<br/>"
        "sns.publish(TopicArn='arn:aws:sns:us-east-1:123:GlobalWorkspaceBroadcast',<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Message=json.dumps({'blackboard_state': 'SHARD_FAILOVER_COMMENCED', 'timestamp': time.time()}))",
        "Never use O(N^2) peer-to-peer agent chatter. Fanout state updates over an SNS topic to a shared Redis board."
    )
    for el in fn36: story.append(el)

    # 37. Evidence Voting
    fn37 = build_function_row(
        "Evidence Voting", "REACTIVE", "#2563EB", "Step Functions Distributed Map Consensus Aggregator",
        "Drift-diffusion neural accumulators accumulating stochastic evidence samples until threshold firing.",
        "# Run N parallel model rollouts and aggregate majority vote in Step Functions<br/>"
        "{'Type': 'Map', 'ItemsPath': '$.prompts', 'MaxConcurrency': 5, 'Iterator': {'Type': 'Task', ...}, 'ResultPath': '$.votes'}",
        "Run parallel Bedrock inferences in a Step Functions Map state and select the median/majority answer."
    )
    for el in fn37: story.append(el)

    # 38. Language (Built-in)
    fn38 = build_function_row(
        "Language (Built-in)", "REACTIVE", "#2563EB", "Amazon Bedrock Foundation Models (Native Substrate)",
        "Broca &amp; Wernicke areas translating thoughts into natural language.",
        "# Native capability of LLM foundation model - not an external tool, but the universal cognitive interface<br/>"
        "response = bedrock.converse(modelId='anthropic.claude-3-5-sonnet-20241022-v2:0', messages=conversation)",
        "Language is the native substrate of the foundation model itself; it is the universal cognitive glue."
    )
    for el in fn38: story.append(el)

    # 39. Reads Intent
    fn39 = build_function_row(
        "+ Reads Intent", "PROACTIVE (+)", "#7C3AED", "Bedrock Prompted Theory of Mind (ToM) Projection",
        "Mentalizing network anticipating human unstated goals and emotional intent.",
        "tom_prompt = 'Analyze user intent: Extract unstated goals, hidden constraints, and emotional urgency from: \"' + prompt + '\"'<br/>"
        "intent = bedrock.converse(modelId=MODEL_ID, messages=[{'role':'user', 'content': [{'text': tom_prompt}]}])",
        "Run an intent-projection pass before answering ambiguous prompts to proactively resolve missing context."
    )
    for el in fn39: story.append(el)

    # 40. Stays Aware
    fn40 = build_function_row(
        "+ Stays Aware", "PROACTIVE (+)", "#7C3AED", "CloudWatch Anomaly Detection + Proactive Watcher",
        "Noradrenergic locus coeruleus vigilance system sustaining environmental alertness.",
        "# CloudWatch Anomaly Detection on latency band triggers proactive agent intervention<br/>"
        "cloudwatch.put_metric_alarm(AlarmName='VigilanceWatcher', MetricName='ApiLatency', EvaluationPeriods=2, ThresholdMetricId='ad1')",
        "Proactive watcher agents monitor metric bands and wake the primary agent before users notice outages."
    )
    for el in fn40: story.append(el)

    # 41. Consciousness
    fn41 = build_function_row(
        "? Consciousness", "RESEARCH (?)", "#D97706", "Global Neuronal Workspace Unified State Aggregator",
        "Subjective phenomenal experience ('what it is like to be') and unified access awareness.",
        "# GNW Access Consciousness: Aggregates active perception, working memory, and current goal into a unified state<br/>"
        "conscious_state = {'active_percept': percept, 'working_memory': wm, 'active_goal': goal, 'epistemic_confidence': conf}",
        "While phenomenal consciousness remains open, access consciousness is built by aggregating unified state."
    )
    for el in fn41: story.append(el)

    # =========================================================================
    # PAGE 8: END-TO-END DEPLOYMENT BLUEPRINT
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>End-to-End AWS Multi-Agent Architecture Blueprint</b>", s_h1))
    story.append(Paragraph("How to assemble all 41 functions into an enterprise-ready AWS serverless stack in an afternoon.", s_subtitle))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=8, spaceBefore=4))

    deploy_code = (
        "<font color='#38BDF8'># deploy_brain_stack.py &middot; Quickstart Reference</font><br/>"
        "import boto3, json<br/><br/>"
        "# 1. Initialize AWS Cognitive Substrates<br/>"
        "bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')<br/>"
        "dynamodb = boto3.resource('dynamodb', region_name='us-east-1')<br/>"
        "events = boto3.client('events', region_name='us-east-1')<br/>"
        "sns = boto3.client('sns', region_name='us-east-1')<br/><br/>"
        "# 2. Deploy Society of Mind Agents (6 Pillar Agents)<br/>"
        "PILLAR_AGENTS = {<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Perceptor': {'pillar': 'Perceive', 'thalamus_rule': 'ThalamicGate', 'model': 'claude-3-5-sonnet'},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Memory': {'pillar': 'Remember', 'store': 'DynamoDB_Episodic', 'ttl_enabled': True},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Executive': {'pillar': 'Think', 'planner': 'StepFunctions_DAG', 'guardrail': 'SafetyVeto'},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Affective': {'pillar': 'Learn', 'somatic_alarm': 'CloudWatch_Composite', 'rpe_metric': True},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Motor': {'pillar': 'Act', 'executor': 'Lambda_ToolRunner', 'quota_governor': 'WAF'},<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;'Workspace': {'pillar': 'Connect', 'blackboard': 'Redis_ElastiCache', 'fanout_topic': 'GWS_Broadcast'}<br/>"
        "}<br/><br/>"
        "# 3. Execute Global Workspace Conscious Cycle<br/>"
        "def execute_cognitive_cycle(raw_telemetry):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# Step 1: Perception Agent filters noise<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;gated_signal = perception_agent.filter(raw_telemetry)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# Step 2: Memory Agent binds variables &amp; retrieves past episodes<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;context = memory_agent.retrieve_and_bind(gated_signal)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# Step 3: Affective Agent calculates urgency threat rating<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;urgency_score = affective_agent.evaluate_threat(context)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# Step 4: Executive Judge evaluates metacognitive confidence &amp; plans DAG<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;plan = executive_judge.evaluate_and_plan(context, urgency_score)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# Step 5: Motor Governor executes verified tool call<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;result = motor_governor.execute_action(plan)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;# Step 6: Workspace Hub broadcasts resolution to all agents simultaneously<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;workspace_hub.broadcast_state({'status': 'RESOLVED', 'result': result})"
    )

    story.append(Table([[Paragraph(deploy_code, s_code)]],
                       colWidths=[540],
                       style=[
                           ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
                           ('PADDING', (0,0), (-1,-1), 8),
                           ('BOX', (0,0), (-1,-1), 1, C_AWS_ORANGE),
                       ]))
    story.append(Spacer(1, 12))

    summary_card = [
        [Paragraph("<b>🚀 Key Takeaway for AWS Builders:</b><br/>"
                   "• <b>21 Reactive Functions:</b> Standardize on Amazon Bedrock Converse API tool calling and DynamoDB.<br/>"
                   "• <b>7 Proactive Functions (+):</b> Wire EventBridge Rules and CloudWatch Alarms to wake agents before users complain.<br/>"
                   "• <b>1 Partly (Metacognition):</b> Use structured verbalized confidence scoring and human-in-the-loop escalation.<br/>"
                   "• <b>7 Not Yet:</b> Bridge with DynamoDB TTL (Forgetting) and CloudWatch Composite Alarms (Emotion).<br/>"
                   "• <b>5 Research (?):</b> Experiment with Bedrock token logprob surprise (Predictive Coding) and offline cron replay (Sleep).", s_body)]
    ]
    t_summary = Table(summary_card, colWidths=[540])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (0,0), 1, colors.HexColor("#3B82F6")),
        ('PADDING', (0,0), (0,0), 8),
    ]))
    story.append(t_summary)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated PDF: {PDF_PATH}")

if __name__ == "__main__":
    create_guide_pdf()
