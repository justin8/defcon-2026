package helpers

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"sigs.k8s.io/controller-runtime/pkg/client/fake"

	pocketidv1alpha1 "github.com/aclerici38/pocket-id-operator/api/v1alpha1"
)

func TestResolveStringValue_DirectValue(t *testing.T) {
	scheme := runtime.NewScheme()
	_ = corev1.AddToScheme(scheme)
	client := fake.NewClientBuilder().WithScheme(scheme).Build()
	ctx := context.Background()

	sv := pocketidv1alpha1.StringValue{
		Value: "direct-value",
	}

	result, err := ResolveStringValue(ctx, client, nil, "default", sv, "", "")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != "direct-value" {
		t.Errorf("expected 'direct-value', got '%s'", result)
	}
}
