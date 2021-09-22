{{/*
Expand the name of the chart.
*/}}
{{- define "coalitieakkoordentool.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "coalitieakkoordentool.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create unified labels for coalitieakkoordentool components
*/}}
{{- define "coalitieakkoordentool.common.matchLabels" -}}
app: {{ template "coalitieakkoordentool.name" . }}
release: {{ .Release.Name }}
{{- end -}}

{{- define "coalitieakkoordentool.common.metaLabels" -}}
chart: {{ template "coalitieakkoordentool.chart" . }}
heritage: {{ .Release.Service }}
{{- end -}}

{{- define "coalitieakkoordentool.labels" -}}
{{ include "coalitieakkoordentool.matchLabels" . }}
{{ include "coalitieakkoordentool.common.metaLabels" . }}
{{- end -}}

{{- define "coalitieakkoordentool.matchLabels" -}}
component: {{ .Values.name | quote }}
{{ include "coalitieakkoordentool.common.matchLabels" . }}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "coalitieakkoordentool.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Return the appropriate apiVersion for deployment.
*/}}
{{- define "deployment.apiVersion" -}}
{{- print "apps/v1" -}}
{{- end -}}
{{/*

{{/*
Return the appropriate apiVersion for ingress.
*/}}
{{- define "ingress.apiVersion" -}}
{{- print "networking.k8s.io/v1" -}}
{{- end -}}

{{/*
Define the coalitieakkoordentool.namespace template if set with forceNamespace or .Release.Namespace is set
*/}}
{{- define "coalitieakkoordentool.namespace" -}}
{{- if .Values.forceNamespace -}}
{{ printf "namespace: %s" .Values.forceNamespace }}
{{- else -}}
{{ printf "namespace: %s" .Release.Namespace }}
{{- end -}}
{{- end -}}