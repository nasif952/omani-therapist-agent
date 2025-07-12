import React, { useRef, useState } from "react";

const WS_URL = "ws://localhost:8000/ws/audio"; // Change if running elsewhere

export default function MicStreamTranscriber() {
  const [transcript, setTranscript] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [aiResponse, setAiResponse] = useState("");
  const [isTTSPlaying, setIsTTSPlaying] = useState(false);
  const [messages, setMessages] = useState<{ sender: "me" | "ai"; text: string }[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const ttsAudioChunks = useRef<string[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        } 
      });
      mediaStreamRef.current = stream;
      
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket opened');
        
        // Set up Web Audio API for PCM capture
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)({
          sampleRate: 16000
        });
        audioContextRef.current = audioContext;
        
        const source = audioContext.createMediaStreamSource(stream);
        const processor = audioContext.createScriptProcessor(4096, 1, 1);
        processorRef.current = processor;
        
        processor.onaudioprocess = (e) => {
          if (ws.readyState === WebSocket.OPEN) {
            const inputData = e.inputBuffer.getChannelData(0);
            // Convert float32 to int16 PCM
            const pcmData = new Int16Array(inputData.length);
            for (let i = 0; i < inputData.length; i++) {
              pcmData[i] = Math.max(-32768, Math.min(32767, inputData[i] * 32768));
            }
            console.log('Sending PCM audio chunk of size', pcmData.byteLength);
            ws.send(pcmData.buffer);
          }
        };
        
        source.connect(processor);
        processor.connect(audioContext.destination);
        
        setIsRecording(true);
      };

      ws.onclose = () => {
        console.log('WebSocket closed');
        setIsRecording(false);
        stopAudioCapture();
      };

      ws.onerror = (e) => {
        console.error('WebSocket error', e);
      };

      ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === "partial_transcript" || msg.type === "final_transcript") {
          console.log("Transcription:", msg.text);
          setTranscript((prev) =>
            msg.type === "final_transcript"
              ? prev + " " + msg.text
              : prev.replace(/\[.*?\]$/, "") + " [" + msg.text + "]"
          );
          if (msg.type === "final_transcript") {
            setMessages((prev) => [...prev, { sender: "me", text: msg.text }]);
          }
        } else if (msg.type === "ai_response") {
          console.log("AI Response:", msg.text);
          setAiResponse(msg.text);
          setMessages((prev) => [...prev, { sender: "ai", text: msg.text }]);
        } else if (msg.type === "tts_start") {
          console.log("TTS streaming started");
          ttsAudioChunks.current = [];
          setIsTTSPlaying(false);
        } else if (msg.type === "tts_audio") {
          console.log("Received TTS audio chunk");
          ttsAudioChunks.current.push(msg.chunk);
        } else if (msg.type === "tts_end") {
          console.log("TTS streaming ended, playing audio");
          playTTSBufferedAudio();
        } else if (msg.type === "error") {
          console.error("Backend error:", msg.text);
        }
      };
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopAudioCapture = () => {
    if (processorRef.current) {
      processorRef.current.disconnect();
      processorRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop());
      mediaStreamRef.current = null;
    }
  };

  const stopRecording = () => {
    wsRef.current?.close();
    setIsRecording(false);
    stopAudioCapture();
  };

  const playTTSBufferedAudio = async () => {
    if (ttsAudioChunks.current.length === 0) return;
    setIsTTSPlaying(true);
    
    try {
      // Concatenate all base64 chunks
      const combinedBase64 = ttsAudioChunks.current.join('');
      
      // Convert base64 to binary
      const binaryString = atob(combinedBase64);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      
      // Create audio blob and play
      console.log('First 16 bytes of TTS audio:', Array.from(bytes.slice(0, 16)));
      const blob = new Blob([bytes], { type: 'audio/mp3' });
      const audioUrl = URL.createObjectURL(blob);
      console.log('TTS audio blob size:', blob.size, 'type:', blob.type);
      window.open(audioUrl, '_blank'); // Open in new tab for manual test
      const audio = new Audio(audioUrl);
      
      audio.onended = () => {
        setIsTTSPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
      
      audio.onerror = (e) => {
        console.error('Audio playback error:', e);
        setIsTTSPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
      
      console.log('Playing TTS audio...');
      await audio.play();
    } catch (e) {
      setIsTTSPlaying(false);
      console.error('Error playing TTS audio', e);
    }
  };

  return (
    <div>
      <h2>Live Omani Arabic Transcription</h2>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? "Stop" : "Start"} Recording
      </button>
      <div style={{ marginTop: 20, whiteSpace: "pre-wrap" }}>
        <strong>Transcript:</strong>
        <div>{transcript}</div>
      </div>
      <div style={{ marginTop: 20 }}>
        <strong>Chat History:</strong>
        <div style={{
          maxHeight: 300,
          overflowY: 'auto',
          background: '#f5f5f5',
          borderRadius: 8,
          padding: 12,
          marginTop: 8,
          marginBottom: 8,
        }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{
              display: 'flex',
              justifyContent: msg.sender === 'me' ? 'flex-end' : 'flex-start',
              marginBottom: 8
            }}>
              <div style={{
                background: msg.sender === 'me' ? '#d1e7dd' : '#fff',
                color: '#222',
                borderRadius: 16,
                padding: '8px 16px',
                maxWidth: '70%',
                boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
                fontWeight: msg.sender === 'me' ? 500 : 400
              }}>
                <span style={{ fontSize: 12, color: '#888', marginRight: 8 }}>
                  {msg.sender === 'me' ? 'Me' : 'AI Therapist'}:
                </span>
                {msg.text}
              </div>
            </div>
          ))}
        </div>
      </div>
      {isTTSPlaying && (
        <div style={{ marginTop: 10, color: 'green' }}>
          🔊 Playing AI response...
        </div>
      )}
    </div>
  );
} 