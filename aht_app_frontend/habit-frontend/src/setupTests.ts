/// <reference types="vitest/globals" />
import "@testing-library/jest-dom";
import { server } from "./tests/msw/server";

// Start MSW before all tests
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
